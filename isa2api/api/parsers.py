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
session_arguments.add_argument('server', type=int, required=True, help='Server id')
session_arguments.add_argument('sort', type=str, required=False, default='timestamp', choices=['timestamp', 'id', 'caller', 'called'], help='column to order by')
session_arguments.add_argument('order', type=str, required=False, default='desc', choices=['asc', 'desc'], help='order direction')


fromTo_arguments = reqparse.RequestParser()
fromTo_arguments.add_argument('server', type=int, required=True, default=-1, help='Server id')
fromTo_arguments.add_argument('fromDate', type=str, required=False, default=yesterday.isoformat(), help='Iso format')
fromTo_arguments.add_argument('toDate', type=str, required=False , default=date.today().isoformat(),help='Iso format')


login_arguments = reqparse.RequestParser()
login_arguments.add_argument('username', type=str, required=True, help='username', location='json')
login_arguments.add_argument('password', type=str, required=True,  help='password', location='json')


token_arguments = reqparse.RequestParser()
token_arguments.add_argument('token', type=str, required=False, help='API Token')

paths_arguments = fromTo_arguments.copy()
paths_arguments.add_argument('limit', type=int, required=False, default=10, help='Max number of paths')
