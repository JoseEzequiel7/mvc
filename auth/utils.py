from yourapp.models.user import User

def load_user(user_id):
    """Retorna o usuário com base no ID da sessão."""
    return User.query.get(int(user_id))

