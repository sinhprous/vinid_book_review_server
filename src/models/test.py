from src.models.db_conn import cursor


if __name__ == '__main__':
    uuid = '6940223'
    book_id = '1'
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
    OR review.mode='public') LIMIT 5;" % (str(book_id), str(uuid))
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
                "content": des[0]
            })
    else:
        elements.append({
            "type": "text",
            "style": "paragraph",
            "content": "Chưa có bình luận "
        })
    # for ele in elements:
    #     print(ele)

    query = "SELECT question.id, question.content FROM question WHERE book_id='1' LIMIT 2"
    cursor.execute(query)
    questions = cursor.fetchall()
    print(questions)
