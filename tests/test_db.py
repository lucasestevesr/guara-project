from dataclasses import asdict

from sqlalchemy import select

from guara.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(username='testuser', password='123', email='test@test')
        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == 'testuser'))

    assert asdict(user) == {
        'id': 1,
        'username': 'testuser',
        'password': '123',
        'email': 'test@test',
        'created_at': time,
    }
