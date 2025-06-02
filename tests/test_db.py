from dataclasses import asdict

from sqlalchemy import select

from guara.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='Gdel', password='secret', email='Gdel@gmail.com'
        )
        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == 'Gdel'))

    assert asdict(user) == {
        'id': 1,
        'username': 'Gdel',
        'password': 'secret',
        'email': 'Gdel@gmail.com',
        'created_at': time,
        'updated_at': time,
    }
