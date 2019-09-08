from flask import request, Blueprint, Response, jsonify, render_template, send_file
import qrcode
from src.models.db_conn import cursor
form_review = Blueprint("form_review", __name__, template_folder="templates")
import json


def valid_user(uuid):
    query = \
        "INSERT INTO reader (name, age, email, account, `password`, user_rank) \
        VALUES ('', 4, '', '%s', '', '')" % str(uuid)
    print(query)
    cursor.execute(query)


@form_review.route("/render_spoil_review", methods=["POST"])
def book_review():
    params = request.args
    json_body = request.json
    # print ('params', params)
    # print ('json body', request.json)
    book_id = params.get("book_id")
    uuid = request.headers.get('user_id')
    question_ids = []
    answer_ids = []
    
    for k, v in dict(params).items():
        if 'qid' in k:
            i = int(k.replace('qid', ''))
            qid = params.get(k) # id cua cau hoi thu i
            question_ids.append(qid) 
            aid = json_body.get(str(i+1)) # answer cau hoi thu i cua user, "1" la A, "2" la B, "3" la C
            answer_ids.append(aid)

    print(question_ids, answer_ids)
    question_ids_condition = "".join([" (question.id='%s' AND question.answer='%s') OR " % (str(qid), str(aws))
                                      for qid, aws in zip(question_ids, answer_ids)]) + "1=0"
    query = "SELECT question.id, question.answer from question WHERE " + question_ids_condition
    cursor.execute(query)
    answer_sheet=cursor.fetchall()
    if len(answer_sheet) == len(answer_ids):
        # TODO: if tra loi dung ca 2
        query = "SELECT id, account FROM reader WHERE account='%s'" % str(uuid)
        print(query)
        cursor.execute(query)
        rs = cursor.fetchall()
        if len(rs) == 0:
            #chua ton tai trong db
            valid_user(uuid)
            query = "SELECT id, account FROM reader WHERE account='%s'" % str(uuid)
            print(query)
            cursor.execute(query)
            rs = cursor.fetchall()
        reader_id = rs[0][0]
        query = \
            "INSERT INTO library (user_id, book_id, mode) \
            SELECT * FROM (SELECT '%s', '%s', 'read') AS tmp \
            WHERE NOT EXISTS( \
            SELECT user_id FROM library WHERE user_id='%s' AND book_id='%s' \
            ) LIMIT 1;" %(str(reader_id), str(book_id), str(reader_id), str(book_id))
        print(query)
        cursor.execute(query)
        cursor.execute("COMMIT")
        #haipham
        query = "SELECT cover FROM book WHERE book.id='%s';" % str(book_id)
        cursor.execute(query)
        cover = cursor.fetchone()
        query = \
            "SELECT content FROM review_detail, review, reader \
            WHERE review_detail.id = review.review_detail_id \
            AND review.book_id='%s' \
            AND reader.id = review.user_id \
            AND (reader.account='%s' \
            OR review.mode='public') ORDER BY RAND() LIMIT 5;" % (str(book_id), str(uuid))
        cursor.execute(query)
        descriptions = cursor.fetchall()
        elements = []
        if cover is not None and len(cover) > 0:
            elements.append({
                "type": "web",
                "content": cover[0]
            })
        if descriptions is not None and len(descriptions):
            for des in descriptions:
                elements.append({
                    "type": "text",
                    "style": "paragraph",
                    "content": '• '+des[0]
                })
        else:
            elements.append({
                "type": "text",
                "style": "paragraph",
                "content": "Chưa có bình luận "
            })
        
        elements.append({
            "type": "input",
            "input_type": "textarea",
            "name": "review",
            "required": "true",
            "placeholder": "Viết review của bạn cho chúng tôi"
        })
        elements.append({
            "type": "radio",
            "display_type": "inline",
            "required": "true",
            "label": "Có công khai review này không",
            "name": "is_public",
            "options": [
                {
                    "label": "Không",
                    "value": 0
                },
                {
                    "label": "Có",
                    "value": 1
                }
            ]
        })

        print ("bug, ", elements)
        result = {
            "data": {
                "metadata": {
                    "app_name": "Book Review",
                    "app_id": 123456,
                    "title": "Đánh giá nổi bật",
                    "submit_button": {
                        "label": "Gửi đánh giá",
                        "background_color": "#6666ff",
                        "cta": "request",
                        "url": "http://35.234.201.74:5000/review_done?book_id=%s" % book_id
                    },
                    "reset_button": {
                        "label": "Xóa toàn bộ",
                        "background_color": "#669999"
                    },
                    "elements": elements
                }
            }
        }

    # TODO: if tra loi sai it nhat 1 cau, hien ra man hinh: chi co nguoi da doc sach moi duoc xem review spoil
    else:
        result = {
            "data": {
                "metadata": {
                    "app_name": "Book Review",
                    "app_id": 123456,
                    "title": "Đánh giá nổi bật",
                    "submit_button": {
                        "label": "Thoát",
                        "background_color": "#6666ff",
                        "cta": "close",
                    },
                    # "reset_button": {
                    #     "label": "Xóa toàn bộ",
                    #     "background_color": "#669999"
                    # },
                    "elements": [
                        {
                            "type": "text",
                            "style": "heading",
                            "content": "Đánh giá của mọi người"
                        },
                        {
                            "type": "text",
                            "style": "paragraph",
                            "content": "Chỉ có người đã đọc sách mới được xem review chi tiết"
                        },
                    ]
                }
            }
        }
    return jsonify(result), 200


@form_review.route("/render_public_review", methods=["POST"])
def book_public():
    uuid = request.headers.get('user_id')
    params = request.args
    book_id = params.get("book_id")
    print('uuid: %s, bookid: %s' % (str(uuid), str(book_id)))
    query = "SELECT cover FROM book WHERE book.id='%s';" % str(book_id)
    cursor.execute(query)
    cover = cursor.fetchone()
    query = \
        "SELECT content FROM review_detail, review, reader \
        WHERE review_detail.id = review.review_detail_id \
        AND review.book_id='%s' \
        AND review_detail.category='non_spoil' \
        AND reader.id = review.user_id \
        AND (reader.account='%s' \
        OR review.mode='public') ORDER BY RAND() LIMIT 5;" % (str(book_id), str(uuid))
    cursor.execute(query)
    descriptions = cursor.fetchall()
    elements = []
    if cover is not None and len(cover) > 0:
        elements.append({
            "type":"web",
            "content": cover[0]
        })
        print (cover)
    # NOTE: man hinh dau tien, chi show 1 nhan xet noi bat nhat.    
    if descriptions is not None and len(descriptions):
        max_i = 0; max_l = 0
        for i, des in enumerate(descriptions):
            if len(des[0]) > max_l:
                max_l = len(des[0])
                max_i = i
        elements.append({
            "type": "text",
            "style": "paragraph",
            "content": descriptions[max_i][0]
        })
    else:
        elements.append({
            "type": "text",
            "style": "paragraph",
            "content": "Chưa có bình luận "
        })
    
    elements.append(
        {
            "type": "input",
            "input_type": "textarea",
            "name": "review"
        }
    )

    print ("elements: ", elements)
    result = {
        "data": {
            "metadata": {
                "app_name": "Book Review",
                "app_id": 123456,
                "title": "Đánh giá nổi bật",
                "submit_button": {
                    "label": "Xem spoil review",
                    "background_color": "#6666ff",
                    "cta": "request",
                    "url": "http://35.234.201.74:5000/answer?book_id=%s" % book_id
                },
                "elements": elements
            }
        }
    }
    return jsonify(result), 200


@form_review.route('/answer', methods=['POST'])
def answer():
    uuid = request.headers.get('user_id')
    params = request.args
    book_id = params.get('book_id')
    query = \
    "SELECT mode FROM library, reader \
    WHERE reader.account='%s' \
    AND library.user_id= reader.id \
    AND book_id='%s'" % (uuid, book_id)
    cursor.execute(query)
    is_book_read = cursor.fetchone()

    query = "SELECT cover FROM book WHERE book.id='%s';" % str(book_id)
    cursor.execute(query)
    cover = cursor.fetchone()
    query = \
        "SELECT content FROM review_detail, review, reader \
        WHERE review_detail.id = review.review_detail_id \
        AND review.book_id='%s' \
        AND reader.id = review.user_id \
        AND (reader.account='%s' \
        OR review.mode='public') ORDER BY RAND() LIMIT 5;" % (str(book_id), str(uuid))
    cursor.execute(query)
    descriptions = cursor.fetchall()
    all_reviews = ''
    if descriptions is not None and len(descriptions):
        for des in descriptions:
            all_reviews += '• '+des[0]+'\n'
    # NOTE: if user have read this book (should be moved to /render_spoil_review)

    if is_book_read is not None and is_book_read[0] == "read":
        result = {
            "data": {
                "metadata": {
                    "app_name": "Book Review",
                    "app_id": 123456,
                    "title": "Đánh giá nổi bật",
                    "submit_button": {
                        "label": "Gửi đánh giá",
                        "background_color": "#6666ff",
                        "cta": "request",
                        "url": "http://35.234.201.74:5000/review_done?book_id=%s" % book_id
                    },
                    "reset_button": {
                        "label": "Xóa toàn bộ",
                        "background_color": "#669999"
                    },
                    "elements": [
                        {
                            "type": "text",
                            "style": "heading",
                            "content": "Đánh giá của mọi người"
                        },
                        {
                            "type": "text",
                            "style": "paragraph",
                            "content": all_reviews
                        },
                        {
                            "type": "input",
                            "input_type": "textarea",
                            "name": "review",
                            "required": "true",
                            "placeholder": "Viết review của bạn cho chúng tôi"
                        },
                        {
                            "type": "radio",
                            "display_type": "inline",
                            "required": "true",
                            "label": "Có công khai review này không",
                            "name": "is_public",
                            "options": [
                                {
                                    "label": "Không",
                                    "value": 0
                                },
                                {
                                    "label": "Có",
                                    "value": 1
                                }
                            ]
                        }
                    ]
                }
            }
        }
        return jsonify(result), 200
    else:
        query = "SELECT question.id, question.content FROM question WHERE book_id='%s' ORDER BY RAND() LIMIT 2" % book_id
        cursor.execute(query)
        questions = cursor.fetchall()
        elements = []
        question_ids = []
        for question_index in range(0, len(questions)):
            tmp_obj = questions[question_index][1].split("\\n")
            tmp_json = {
                            "type": "radio",
                            "display_type": "inline",
                            "required": "true",
                            "label": tmp_obj[0],
                            "name": questions[question_index][0],
                            "options": [
                                {
                                    "label": tmp_obj[i],
                                    "value": i
                                }
                                for i in range(1, len(tmp_obj))
                            ]
                        }
            elements.append(tmp_json)
            question_ids.append(questions[question_index][0])
        
        url = 'http://35.234.201.74:5000/render_spoil_review?book_id=%s'% book_id
        for i in range(len(question_ids)):
            url += '&qid%d=%s'% (i, question_ids[i])
        result = {
            'data': {
                'metadata': {
                    'app_name': 'Book Review',
                    'app_id': 123456,
                    'title': 'Xác nhận đã đọc sách',
                    'submit_button': {
                        'label': 'Xem spoil review',
                        'background_color': '#6666ff',
                        'cta': 'request',
                        'url': url
                    },
                    'elements': elements
                }
            }
        }
        return jsonify(result), 200


@form_review.route("/review_done", methods=["POST"])
def review():
    data = request.data
    params = request.args
    book_id = params.get("book_id")
    print(params)
    print(data)
    dict_data = json.loads(data.decode(), encoding="utf-8")
    user_review = dict_data.get("review")
    public_mode = dict_data.get("is_public")
    mode = 'public' if public_mode is not None and str(public_mode) == '1' else 'private'
    uuid = request.headers.get('user_id')
    query = "SELECT id, account FROM reader WHERE account='%s'" % str(uuid)
    print(query)
    cursor.execute(query)
    rs = cursor.fetchall()
    if len(rs) == 0:
        # chua ton tai trong db
        valid_user(uuid)
        query = "SELECT id, account FROM reader WHERE account='%s'" % str(uuid)
        print(query)
        cursor.execute(query)
        rs = cursor.fetchall()
    reader_id = rs[0][0]
    query = "INSERT INTO review_detail (content, category) VALUES ('%s', 'non_spoil')" % user_review
    cursor.execute(query)
    query = "SELECT LAST_INSERT_ID()"
    cursor.execute(query)
    review_detail_last_id = cursor.fetchone()[0]
    query = \
        "INSERT INTO review (mode, user_id, book_id, review_detail_id) \
        VALUES ('%s', '%s', '%s', '%s')" % (mode, str(reader_id), str(book_id), str(review_detail_last_id))
    cursor.execute(query)
    cursor.execute("COMMIT")
    # return Response(status=200)
    result = {
        "data": {
            "metadata": {
                "app_name": "Book Review",
                "app_id": 123456,
                "title": "Đánh giá nổi bật",
                "elements": [
                    {
                        "type": "text",
                        "style": "heading",
                        "content": "Đánh giá của bạn"
                    },
                    {
                        "type": "text",
                        "style": "paragraph",
                        "content": "Đánh giá của bạn đã được gửi"
                    }
                ]
            }
        }
    }
    return jsonify(result), 200



@form_review.route("/genqr", methods=["POST", "GET"])
def gen_qr():
    if request.method == "GET":
        return render_template('genqr.html')
    elif request.method == "POST":
        book_name = request.form['book']
        author_name = request.form['author']
        year = request.form['year']
        cover = request.form['cover']
        print(book_name, author_name, year)

        cover = '<html><body><h2>{}</h2><img src="{}" alt="Trulli" width="100%"></body></html>'.format(book_name, cover)
        query = \
            "INSERT INTO book (publisher, book_name, edition, author, difficulity, cover) \
            VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % ('Kim Đồng', book_name, year, author_name, '1', cover)
        cursor.execute(query)
        new_id = cursor.lastrowid
        print (new_id)
        cursor.execute("COMMIT")

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data('https://qr.id.vin/hook?url=http://35.234.201.74:5000/render_public_review?book_id={}'.format(new_id))
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save('recent_qr.png')

        return send_file('recent_qr.png', mimetype='image/gif')
