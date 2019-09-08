from flask import request, Blueprint, Response, jsonify
from server import app

form_review = Blueprint('form_review', __name__, template_folder='templates')


@form_review.route('/render', methods=['POST'])
def book_review():
    params = request.args
    is_spoil = params.get('is_spoil')
    book_id = params.get('book_id')
    if is_spoil:
        result = {
            'data': {
                'metadata': {
                    'app_name': 'Book Review',
                    'app_id': 123456,
                    'title': 'Đánh giá nổi bật',
                    'submit_button': {
                        'label': 'Gửi đánh giá',
                        'background_color': '#6666ff',
                        'cta': 'close',
                        'url': 'http://35.234.201.74:5000/review?book_id=%s'%book_id
                    },
                    'reset_button': {
                        'label': 'Xóa toàn bộ',
                        'background_color': '#669999'
                    },
                    'elements': [
                        {
                            'type': 'text',
                            'style': 'heading',
                            'content': 'Spoil'
                        },
                        {
                            "type": "input",
                            "input_type": "textarea",
                            "name": "review",
                            "required": "true",
                            "placeholder": "Viết review của bạn cho chúng tôi"
                        }
                    ]
                }
            }
        }
    else:
        result = {
        'data': {
            'metadata': {
                'app_name': 'Book Review',
                'app_id': 123456,
                'title': 'Đánh giá nổi bật',
                'submit_button': {
                    'label': 'Gửi đánh giá',
                    'background_color': '#6666ff',
                    'cta': 'request',
                    'url': 'http://35.234.201.74:5000/review?bookid=123'
                },
                'reset_button': {
                    'label': 'Xóa toàn bộ',
                    'background_color': '#669999'
                },
                'elements': [
                    {
                        'type': 'text',
                        'style': 'heading',
                        'content': 'Đánh giá của bạn'
                    },
                    {
                        "type":"radio",
                        "dispay_type": "dialog",
                        "required": "true",
                        "label": "Câu hỏi 1",
                        "name": "question_1",
                        "options": [
                            {
                                "label": "Dap an 1",
                                "value": 1
                            },
                            {
                                "label": "Dap an 2",
                                "value": 2
                            }
                        ]
                    },
                    {
                        "type":"radio",
                        "dispay_type": "dialog",
                        "required": "true",
                        "label": "Câu hỏi 2",
                        "name": "question_2",
                        "options": [
                            {
                                "label": "Dap an 1",
                                "value": 1
                            },
                            {
                                "label": "Dap an 2",
                                "value": 2
                            }
                        ]
                    },
                    {
                        "type":"radio",
                        "dispay_type": "dialog",
                        "required": "true",
                        "label": "Câu hỏi 3",
                        "name": "question_3",
                        "options": [
                            {
                                "label": "Dap an 1",
                                "value": 1
                            },
                            {
                                "label": "Dap an 2",
                                "value": 2
                            }
                        ]
                    },
                    {
                        "type":"input",
                        "input_type": "textarea",
                        "name": "review",
                        "required": "true",
                        "placeholder": "Viết review của bạn cho chúng tôi"
                    }
                ]
            }
        }
    }
    return jsonify(result), 200

@form_review.route('/answer', methods=['POST'])
def answer():
    params = request.args
    book_id = params.get('book_id')
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
                    'url': 'http://35.234.201.74:5000/render?book_id=%s' % book_id
                },
                'elements': [
                    {
                        "type": "radio",
                        "dispay_type": "dialog",
                        "required": "true",
                        "label": "Câu hỏi 1",
                        "name": "question_1",
                        "options": [
                            {
                                "label": "Dap an 1",
                                "value": 1
                            },
                            {
                                "label": "Dap an 2",
                                "value": 2
                            }
                        ]
                    },
                    {
                        "type": "radio",
                        "dispay_type": "dialog",
                        "required": "true",
                        "label": "Câu hỏi 2",
                        "name": "question_2",
                        "options": [
                            {
                                "label": "Dap an 1",
                                "value": 1
                            },
                            {
                                "label": "Dap an 2",
                                "value": 2
                            }
                        ]
                    },
                    {
                        "type": "radio",
                        "dispay_type": "dialog",
                        "required": "true",
                        "label": "Câu hỏi 3",
                        "name": "question_3",
                        "options": [
                            {
                                "label": "Dap an 1",
                                "value": 1
                            },
                            {
                                "label": "Dap an 2",
                                "value": 2
                            }
                        ]
                    }
                ]
            }
        }
    }
    return jsonify(result), 200


@form_review.route('/review', methods=['POST'])
def review():
    uuid = request.headers.get('user_id')
    print("uuid: %s" % str(uuid))
    data = request.data
    params = request.args
    book_id = params.get('book_id')
    is_get_review = params.get('is_get_review')
    if is_get_review is not None:
        return
    print(params)
    print(data)
    return Response(status=200)
