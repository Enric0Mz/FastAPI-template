from src.infra.security.password import hash_password


def test_size_of_hash_password_function_for_diferent_inputs():
    password1 = "TestePassowrdResultSize"
    password2 = "TPRS"
    password3 = "1"
    password4 = "HASHHASHHASHHAHhahshahshahshshahshahshahshahshahshahsh"

    hashed_password1 = hash_password(password1)
    hashed_password2 = hash_password(password2)
    hashed_password3 = hash_password(password3)
    hashed_password4 = hash_password(password4)

    assert len(hashed_password1) == 97
    assert len(hashed_password2) == 97
    assert len(hashed_password3) == 97
    assert len(hashed_password4) == 97
