from database_connection import get_database_connection
from repositories.question_repository import QuestionRepository
from entities.quiz import Quiz


def initialize_questions(connection=None, question_repository=None) -> object:
    """Initializes the questions for the quiz, with reaady-to-use questions.

    Args:
        connection: 
            Object to use as connection for quiz.
        question_repository: 
            Class, which handles the database operations for the questions.
    """

    if connection is None:
        connection = get_database_connection()

    if question_repository is None:
        question_repository = QuestionRepository(connection)

    cursor = connection.cursor()
    cursor.execute("DELETE FROM questions")
    connection.commit()

    questions = [
        Quiz(None, "What is the largest planet in the Solar system?",
                ["Mars", "Pluto", "Jupiter", "Venus"], "Jupiter"),

        Quiz(None, "What is the capital of Australia?", [
            "Perth", "Sidney", "Canberra", "Melbourne"], "Canberra"),

        Quiz(None, "Who won the icehockey World cup in 1995?", [
            "USA", "Sweden", "Finland", "Canada"], "Finland"),

        Quiz(None, "In what year Finland participated in the football European cup?", [
            "1992", "2002", "2022", "2021"], "2021"),

        Quiz(None, "In what year Finland won the Eurovision song contest?", [
            "1996", "1998", "2012", "2006"], "2006"),

        Quiz(None, "What is the largest lake in Finland?", [
            "Päijänne", "Saimaa", "Oulujärvi", "Inarijärvi"], "Saimaa"),
    ]

    for quiz in questions:
        question_repository.create_question(quiz)
    print('Questions initialized for the quiz, you can start playing!')


if __name__ == "__main__":
    initialize_questions()
