from dataclasses import dataclass

from dto.user.intro_user import IntroUserDto


class UserDto:
    class Request:
        pass

    class Response:
        @dataclass
        class Users:
            users: list[IntroUserDto]
