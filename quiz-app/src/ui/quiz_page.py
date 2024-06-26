from tkinter import ttk, constants
from services.question_service import question_service
from services.user_service import user_service


class QuizPage:
    """Class, which is used for quiz operations."""

    def __init__(self, root, handle_user_page):
        """Constructor for QuizPage class, handles starting a new quiz and logout.

        Args:
            root: 
                Base for tkinter, initializes the app view.
            handle_user_page: 
                Called variable to end quiz and move to user view.
        """

        self._root = root
        self._handle_user_page = handle_user_page
        self._frame = None
        self._user = user_service.get_current_user()
        self._questions = question_service.show_questions()
        self._current_question_index = 0
        self._current_question = None
        self._quiz_ended = False

        self._initialize()

    def pack(self):
        """Showing the view with Tkinter pack-method."""

        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Deletes the current view."""

        self._frame.destroy()

    # Generated code starts
    def _show_quiz_questions(self):
        if self._current_question:
            self._current_question.grid_forget()

        if self._current_question_index < len(self._questions):
            current_question = self._questions[self._current_question_index]
            question_label = ttk.Label(
                master=self._frame,
                text=current_question.question
            )
            question_label.grid(row=1, column=0, columnspan=2,
                                padx=5, pady=10, sticky="N")
            self._current_question = question_label

            for i, option in enumerate(current_question.options):
                button_width = 20
                row = (i // 2) + 2
                column = i % 2
                option_button = ttk.Button(
                    master=self._frame,
                    text=option,
                    width=button_width,
                    command=lambda idx=i, question=current_question: self._handle_option(
                        question, idx)
                )
                option_button.grid(row=row, column=column, padx=5,
                                   pady=5, sticky="EW")

    def _handle_option(self, question, option_index):
        if not self._quiz_ended:
            selected_option = question.options[option_index]
            is_correct = question_service.check_answer(
                question, selected_option)

            if question.question_id not in self._answered_questions:
                if is_correct:
                    question_service.calculate_points(
                        self._user, question, selected_option)
                    self._answered_questions.add(question.question_id)

            self._current_question_index += 1

            if self._current_question_index < len(self._questions):
                self._show_quiz_questions()
            else:
                self._end_quiz()
    # Generated code ends

    def _end_quiz(self):
        if not self._quiz_ended:
            total_points = question_service.get_points(self._user)
            question_service.update_highscore(self._user)
            ttk.Label(
                master=self._frame,
                text=f"Quiz ended. You scored {total_points}/{len(self._questions)} points."
            ).grid(row=self._current_question_index + 2, column=0, padx=5, pady=10,
                   sticky=constants.W)
            self._quiz_ended = True

    def _initialize_header(self):
        quiz_label = ttk.Label(
            master=self._frame, text=f'Playing as {self._user.username}.')
        quiz_label.grid(row=0, column=0, padx=5, pady=10, sticky=constants.EW)

    def _initialize_user_page(self):
        user_page_button = ttk.Button(
            master=self._frame,
            text="End quiz & return to user page",
            command=self._handle_user_page
        )
        user_page_button.grid(row=0, column=1, padx=5,
                              pady=10, sticky=constants.NE)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        self._initialize_header()
        self._initialize_user_page()
        self._answered_questions = set()
        self._show_quiz_questions()
        self._frame.grid_columnconfigure(0, weight=1, uniform="group1")
        self._frame.grid_columnconfigure(1, weight=1, uniform="group1")
