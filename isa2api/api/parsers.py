from flask_restplus import reqparse
from datetime import date, timedelta

yesterday = date.today() - timedelta(1)
session_arguments = reqparse.RequestParser()
session_arguments.add_argument('page', type=int, required=False, default=1, help='Page number')
session_arguments.add_argument('per_page', type=int, required=False, choices=[10, 20, 30, 40, 50, 100],
                                  default=10, help='Results per page {error_msg}')
session_arguments.add_argument('id', type=str, required=False, help='Session ID')
session_arguments.add_argument('caller', type=str, required=False, help='Caller number')
session_arguments.add_argument('called', type=str, required=False, help='Called number')
session_arguments.add_argument('fromDate', type=str, required=False, default=yesterday.isoformat(), help='Iso format')
session_arguments.add_argument('toDate', type=str, required=False , default=date.today().isoformat(),help='Iso format')
session_arguments.add_argument('server', type=int, required=False, default=-1, help='Server id')
