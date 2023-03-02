import random
import sqlite3

import pygame
import pygame_gui

import data_struct

# ASCII printables (last char in string is space)
x = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&'()*+,-.\/:;<=>?@[]^_`{|}~ "


class TypeMaster:
    # initialize class
    def __init__(self):
        # initialize pygame
        pygame.init()
        # set allowed characters
        self.allowed_characters = [*x]
        # set frame rate
        self.clock = pygame.time.Clock()
        self.time_delta = self.clock.tick(60) / 1000.0
        # set resolution
        self.resolution = (1280, 720)
        self.window_surface = pygame.display.set_mode(self.resolution)
        # set background color
        self.bgcolor = "#121212"
        # set some button constants
        self.button_dim = (270, 64)
        self.back_button_dim = (150, 40)
        self.back_button_pos = (50, 650)
        # set some title constants
        self.title_center = (640, 100)
        self.title_color = "#eaeaea"
        self.title_size = 95
        self.subtitle_size = 45
        self.label_size = 23
        # set session statistics
        self.session_wpm = 0
        self.session_accuracy = 0
        self.session_time = 0
        self.session_typed = 0
        # set passages
        self.keydict = {}
        self.keys = self.get_keys()

    # set a static method to return time elapsed since program start
    @staticmethod
    def get_time():
        return f"{round((pygame.time.get_ticks() / 1000), 3):.3f}"

    # set a static method to load custom fonts
    @staticmethod
    def get_font(size):
        return pygame.font.Font("font.ttf", size)

    # sql functions
    # get dictionary of keys 'id' and values 'passage' from database
    def load_keydict(self):
        self.keydict = {}
        conn = sqlite3.connect("typemaster.db")
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        query = "SELECT * FROM text"
        result = curs.execute(query)
        for r in result.fetchall():
            id = str(r["id"])
            self.keydict[id] = r["passage"]
        conn.commit()
        conn.close()

    # return a list of keys
    def get_keys(self):
        self.load_keydict()
        return list(self.keydict.keys())

    # push queries to database
    def execute_query(self, query):
        conn = sqlite3.connect("typemaster.db")
        curs = conn.cursor()
        curs.execute(query)
        conn.commit()
        conn.close()
        self.load_keydict()

    # function for main menu
    # the screen that allows user to quit and access all the subpages
    def main_menu(self):
        # set up main menu
        main_menu_manager = pygame_gui.UIManager(self.resolution)
        pygame.display.set_caption("main menu")
        main_menu_running = True
        print(f"{self.get_time()}: main menu")
        # titles
        main_menu_title = self.get_font(self.title_size).render(
            "type master", True, self.title_color
        )
        main_menu_title_rect = main_menu_title.get_rect(center=self.title_center)
        # buttons
        play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((505, 380), self.button_dim),
            text="play",
            manager=main_menu_manager,
        )
        stats_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((505, 460), self.button_dim),
            text="session stats",
            manager=main_menu_manager,
        )
        library_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((505, 540), self.button_dim),
            text="manage library",
            manager=main_menu_manager,
        )
        quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.back_button_pos, self.back_button_dim),
            text="quit",
            manager=main_menu_manager,
        )
        # main loop
        while main_menu_running:
            self.window_surface.fill(self.bgcolor)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main_menu_running = False
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    # quit
                    if event.ui_element == quit_button:
                        print(self.get_time() + ": exit")
                        main_menu_running = False
                        quit()
                    # enter play menu
                    if event.ui_element == play_button:
                        self.play_menu()
                        main_menu_running = False
                    # enter stats
                    if event.ui_element == stats_button:
                        self.stats()
                        main_menu_running = False
                    # enter library
                    if event.ui_element == library_button:
                        self.library()
                        main_menu_running = False
                main_menu_manager.process_events(event)
            main_menu_manager.update(self.time_delta)
            self.window_surface.blit(main_menu_title, main_menu_title_rect)
            main_menu_manager.draw_ui(self.window_surface)
            pygame.display.flip()

    # function for play menu.
    # the screen that allows you to:
    #   i)   select(possibly randomly) & preview texts from the database;
    #   ii)  upload one-time custom texts;
    #   iii) return  to the homepage
    def play_menu(self):
        # set up play menu
        play_menu_manager = pygame_gui.UIManager(self.resolution)
        pygame.display.set_caption("play menu")
        play_menu_running = True
        print(f"{self.get_time()}: play menu")
        # titles
        # play menu main title
        play_menu_title = self.get_font(self.subtitle_size).render(
            "take a test", True, self.title_color
        )
        play_menu_title_rect = play_menu_title.get_rect(center=self.title_center)
        # library text subtitle
        library_title = self.get_font(self.label_size).render(
            "library text", True, self.title_color
        )
        library_title_rect = library_title.get_rect(center=(640, 340))
        # custom text subtitle
        custom_title = self.get_font(self.label_size).render(
            "single test custom", True, self.title_color
        )
        custom_title_rect = custom_title.get_rect(center=(640, 450))
        # load keydict dictionary from passage
        self.load_keydict()
        # print keys
        print(self.get_keys())
        # buttons
        # return to main menu
        back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.back_button_pos, self.back_button_dim),
            text="back",
            manager=play_menu_manager,
        )
        # begin test
        ok_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((730, 545), (75, 38)),
            text="ok",
            manager=play_menu_manager,
        )
        # select random passage from datatabse
        random_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((465, 545), (175, 38)),
            text="random library text",
            manager=play_menu_manager,
        )
        # other UI objects
        # selected text preview
        text_preview = pygame_gui.elements.UITextBox(
            html_text=f"{self.keydict['1'][0:29]}",
            relative_rect=pygame.Rect((465, 363), (260, 38)),
            manager=play_menu_manager,
            wrap_to_height=False,
        )
        # dropdown menu
        text_select = pygame_gui.elements.UIDropDownMenu(
            options_list=self.get_keys(),
            starting_option="1",
            relative_rect=pygame.Rect((735, 363), (70, 38)),
            manager=play_menu_manager,
        )
        # text entry line to input custom text
        custom_text = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((465, 480), (340, 38)), manager=play_menu_manager
        )
        # main loop
        while play_menu_running:
            self.window_surface.fill(self.bgcolor)
            for event in pygame.event.get():
                option = text_select.selected_option
                if event.type == quit:
                    play_menu_running = False
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    # back
                    if event.ui_element == back_button:
                        self.main_menu()
                        play_menu_running = False
                    # random text
                    if event.ui_element == random_button:
                        random_key = random.choice(self.get_keys())
                        self.play(self.keydict[random_key])
                        play_menu_running = False
                    # ok button
                    if event.ui_element == ok_button:
                        if len(custom_text.get_text()) > 0:
                            self.play(custom_text.get_text())
                        else:
                            self.play(self.keydict[option])
                        play_menu_running = False
                # drop down menu option changed
                if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    text_preview.set_text(f"{self.keydict[event.text][0:29]}")
                play_menu_manager.process_events(event)
            play_menu_manager.update(self.time_delta)
            self.window_surface.blit(play_menu_title, play_menu_title_rect)
            self.window_surface.blit(library_title, library_title_rect)
            self.window_surface.blit(custom_title, custom_title_rect)
            play_menu_manager.draw_ui(self.window_surface)
            pygame.display.flip()

    # function for play, the screen where the test is actually taken
    # takes a string parameter that will be used as the passage in the test
    def play(self, text):
        # define colors
        correct_c = "#36D14A"
        incorrect_c = "#DB4E40"
        inactive_c = "#898989"
        # save text used
        chosen_text = text
        # set up play
        play_manager = pygame_gui.UIManager(self.resolution)
        pygame.display.set_caption("play")
        play_running = True
        print(f"{self.get_time()}: play")
        # titles
        play_title = self.get_font(self.title_size).render(
            "test", True, self.title_color
        )
        play_title_rect = play_title.get_rect(center=self.title_center)
        # save some statistics about the chosen text
        total_word_count = len(chosen_text.split(" "))
        total_char_count = len([*chosen_text])
        # split values into data structures
        # from user input:
        correct_typed_chars = data_struct.Stack()
        incorrect_typed_chars = data_struct.Stack()
        # from chosen text:
        remaining_chars = data_struct.ChrQueue(chosen_text)
        typed_text = data_struct.TypedQueue()
        # typo counting variable
        typo_count = 0
        # time count variables
        time_count = False
        start_time = 0
        end_time = 0
        # buttons
        back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.back_button_pos, self.back_button_dim),
            text="back",
            manager=play_manager,
        )
        # other UI objects
        # status bar
        type_progress = pygame_gui.elements.UIStatusBar(
            relative_rect=pygame.Rect((150, 505), (980, 50)), manager=play_manager
        )
        # textbox for hotkey display
        hotkey_display = pygame_gui.elements.UITextBox(
            html_text=f"TAB + ENTER: restart<br>TAB + BACKSPACE: back",
            relative_rect=pygame.Rect((215, 636), (200, 66)),
            manager=play_manager,
        )
        # textbox showing how the chosen text compares to typed text
        text_display = pygame_gui.elements.UITextBox(
            html_text=f"<font color={correct_c}>{str(correct_typed_chars)}<font color={incorrect_c}>{str(incorrect_typed_chars)}<font color={inactive_c}>{str(remaining_chars)}",
            relative_rect=pygame.Rect((300, 200), (680, 250)),
            manager=play_manager,
        )
        # textbox showing the raw input text from the user
        text_input = pygame_gui.elements.UITextBox(
            html_text=f"{typed_text}",
            relative_rect=pygame.Rect((150, 575), (980, 50)),
            manager=play_manager,
        )
        # main loop
        while play_running:
            self.window_surface.fill(self.bgcolor)
            # update textbox with every event
            text_display.set_text(
                f"<font color={correct_c}>{str(correct_typed_chars)}<font color={incorrect_c}>{str(incorrect_typed_chars)}<font color={inactive_c}>{str(remaining_chars)}"
            )
            # get events
            for event in pygame.event.get():
                # window closed
                if event.type == pygame.QUIT:
                    play_running = False
                # UI button objected pressed
                # back
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == back_button:
                        self.play_menu()
                        play_running = False
                # if a key is pressed
                if event.type == pygame.KEYDOWN:
                    # begin counting time after first keypress
                    if not time_count:
                        time_count = True
                        start_time = float(self.get_time())
                    if time_count:
                        keys = pygame.key.get_pressed()
                        # restart hotkey
                        if keys[pygame.K_TAB] and keys[pygame.K_RETURN]:
                            print(f"{self.get_time()}: hotkey restart")
                            play_running = False
                            self.play(chosen_text)
                        # back hotkey
                        if keys[pygame.K_TAB] and keys[pygame.K_BACKSPACE]:
                            print(f"{self.get_time()}: hotkey back")
                            play_running = False
                            self.play_menu()
                        # if typed button contains a character in ASCII printables
                        if event.unicode in self.allowed_characters:
                            # add to the end of the typed_text double-ended queue
                            typed_text.enqueue(event.unicode)
                            # if the first in the queue is the same as first item to be typed
                            # and there are no incorrect characters
                            if (
                                    typed_text.peek() == remaining_chars.peek()
                                    and incorrect_typed_chars.is_empty()
                            ):
                                # add the character to the correct characters stack
                                # while removing from the remaining characters queue
                                correct_typed_chars.push(remaining_chars.dequeue())
                                # remove the character from the front of the typed text queue
                                typed_text.dequeue()
                                # update the status bar by calculating the percentage
                                type_progress.percent_full = int((1- (remaining_chars.items_left()/ total_char_count)) * 100)
                            else:
                                # if the first in the queue is NOT the same as the first item to be typed
                                # if the character is a spacebar push an underscore as the spacebar is invisible
                                # remove from typed text queue and add one typo
                                if typed_text.peek() == " ":
                                    incorrect_typed_chars.push("_")
                                    typed_text.dequeue()
                                else:
                                    incorrect_typed_chars.push(typed_text.dequeue())
                                typo_count += 1
                        # allow backspace ONLY if there are typos so you cannot backspace correct chr
                        if (
                                event.key == pygame.K_BACKSPACE
                                and not incorrect_typed_chars.is_empty()
                        ):
                            # remove last typo chr (as stored in stack)
                            incorrect_typed_chars.pop()
                        text_input.set_text(
                            f"{correct_typed_chars}{incorrect_typed_chars}"
                        )
                # if passage is completely typed
                if remaining_chars.is_empty():
                    type_progress.percent_full = 100
                    end_time = float(self.get_time())
                    time_count = False
                    time_taken = round(end_time - start_time, 2)
                    accuracy = round(
                        (total_char_count / (total_char_count + typo_count)) * 100, 2
                    )
                    wpm = round((total_word_count / time_taken) * 60, 2)
                    play_running = False
                    self.results(chosen_text, time_taken, accuracy, wpm)
                # process events
                play_manager.process_events(event)
            # update manager
            play_manager.update(self.time_delta)
            # blit title
            self.window_surface.blit(play_title, play_title_rect)
            # update UI
            play_manager.draw_ui(self.window_surface)
            # update display
            pygame.display.flip()

    # function for results
    # takes parameters typed text, time, accuracy & wpm
    # gives user option to return to main menu or retype the same passage
    # calculates new session statistics
    def results(self, text, time, percent_acc, wpm):
        # change session stats
        self.session_wpm += wpm
        self.session_accuracy += percent_acc
        self.session_time += time
        self.session_typed += 1
        # UI constants
        results_button_dim = (140, 50)
        stats_rect_dim = (250, 50)
        # set up results
        results_manager = pygame_gui.UIManager(self.resolution)
        pygame.display.set_caption("test results")
        results_running = True
        print(f"{self.get_time()}: test results")
        # titles
        results_title = self.get_font(self.subtitle_size).render(
            "test results", True, self.title_color
        )
        results_title_rect = results_title.get_rect(center=self.title_center)
        # buttons
        menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((400, 600), results_button_dim),
            text="return to menu",
            manager=results_manager,
        )
        replay_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((740, 600), results_button_dim),
            text="try again",
            manager=results_manager,
        )
        # other UI objects
        time_display = pygame_gui.elements.UITextBox(
            html_text=f"Your time is: {time}s",
            relative_rect=pygame.Rect((515, 350), stats_rect_dim),
            manager=results_manager,
        )
        accuracy_display = pygame_gui.elements.UITextBox(
            html_text=f"Your accuracy is: {percent_acc}%",
            relative_rect=pygame.Rect((515, 413), stats_rect_dim),
            manager=results_manager,
        )
        wpm_display = pygame_gui.elements.UITextBox(
            html_text=f"Your wpm is: {wpm}",
            relative_rect=pygame.Rect((515, 476), stats_rect_dim),
            manager=results_manager,
        )
        # main results loop
        while results_running:
            self.window_surface.fill(self.bgcolor)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    results_running = False
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == menu_button:
                        self.main_menu()
                        results_running = False
                    if event.ui_element == replay_button:
                        self.play(text)
                        results_running = False
                results_manager.process_events(event)
            results_manager.update(self.time_delta)
            self.window_surface.blit(results_title, results_title_rect)
            results_manager.draw_ui(self.window_surface)
            pygame.display.flip()

    # function for stats
    # screen that allows user to view their current session's:
    #   I)    number of test typed
    #   II)   average wpm per test
    #   III)  average time per test
    #   IV)   average accuracy per time
    def stats(self):
        # if no typed texts handle the div0 error
        if self.session_typed == 0:
            typed = 0
            avgtime = "-"
            avgwpm = "-"
            avgaccuracy = "-"
        # calculate stats
        else:
            typed = self.session_typed
            avgtime = f"{round(self.session_time / self.session_typed, 2)}s"
            avgwpm = f"{round(self.session_wpm / self.session_typed, 2)}"
            avgaccuracy = f"{round(self.session_accuracy / self.session_typed, 2)}%"
        # set up stats
        stats_manager = pygame_gui.UIManager(self.resolution)
        pygame.display.set_caption("session stats")
        stats_running = True
        print(f"{self.get_time()}: stats")
        # titles
        stats_title = self.get_font(self.subtitle_size).render(
            "session stats", True, self.title_color
        )
        stats_title_rect = stats_title.get_rect(center=self.title_center)
        # buttons
        back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.back_button_pos, self.back_button_dim),
            text="back",
            manager=stats_manager,
        )
        # other UI objects
        practice_typed = pygame_gui.elements.UITextBox(
            html_text=f"Number of races: {self.session_typed}",
            relative_rect=pygame.Rect((450, 287), (370, 48)),
            manager=stats_manager,
        )
        average_time_display = pygame_gui.elements.UITextBox(
            html_text=f"Your session average time is: {avgtime}",
            relative_rect=pygame.Rect((450, 350), (370, 48)),
            manager=stats_manager,
        )
        average_wpm = pygame_gui.elements.UITextBox(
            html_text=f"Your session average wpm is: {avgwpm}",
            relative_rect=pygame.Rect((450, 413), (370, 48)),
            manager=stats_manager,
        )
        average_accuracy = pygame_gui.elements.UITextBox(
            html_text=f"Your session average accuracy is: {avgaccuracy}",
            relative_rect=pygame.Rect((450, 476), (370, 48)),
            manager=stats_manager,
        )
        # main stats loop
        while stats_running:
            self.window_surface.fill(self.bgcolor)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stats_running = False
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == back_button:
                        stats_running = False
                        self.main_menu()
                stats_manager.process_events(event)
            stats_manager.update(self.time_delta)
            self.window_surface.blit(stats_title, stats_title_rect)
            stats_manager.draw_ui(self.window_surface)
            pygame.display.flip()

    # function for library
    # provides an interface for user to edit existing passages in database
    # or create a new entry in the database
    def library(self):
        # set up library
        library_manager = pygame_gui.UIManager(self.resolution)
        pygame.display.set_caption("manage library")
        library_running = True
        print(f"{self.get_time()}: library")
        # titles
        manage_library_title = self.get_font(self.subtitle_size).render(
            "manage library", True, self.title_color
        )
        manage_library_title_rect = manage_library_title.get_rect(
            center=self.title_center
        )
        # refresh dictionary
        self.load_keydict()
        # buttons
        back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(self.back_button_pos, self.back_button_dim),
            text="back",
            manager=library_manager,
        )
        # other UI objects
        text_window = pygame_gui.elements.UITextBox(
            html_text=f"{self.keydict['1']}",
            relative_rect=pygame.Rect((300, 200), (680, 250)),
            manager=library_manager,
        )
        text_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((300, 460), (680, 38)), manager=library_manager
        )
        text_entry.set_text_length_limit(730)
        text_entry.set_allowed_characters(self.allowed_characters)
        text_entry.set_text(self.keydict["1"])
        char_window = pygame_gui.elements.UITextBox(
            html_text=f"{len(self.keydict['1'])}",
            relative_rect=pygame.Rect((300, 510), (50, 38)),
            manager=library_manager,
        )
        text_select = pygame_gui.elements.UIDropDownMenu(
            options_list=self.get_keys(),
            starting_option="1",
            relative_rect=pygame.Rect((360, 510), (75, 38)),
            manager=library_manager,
            object_id="text_select",
        )
        save_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((445, 510), (180, 38)),
            text="save changes",
            manager=library_manager,
        )
        new_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((635, 510), (180, 38)),
            text="new passage",
            manager=library_manager,
        )
        play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((825, 510), (155, 38)),
            text="test",
            manager=library_manager,
        )
        # newtext variable
        new_text = False

        # extra apostrophe due to sqlite3 syntaxing
        def add_apostrophes(s):
            result = ""
            for char in s:
                if char == "'":
                    result += "''"
                else:
                    result += char
            return result

        while library_running:
            self.window_surface.fill(self.bgcolor)
            for event in pygame.event.get():
                if event.type == quit:
                    library_running = False
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == back_button:
                        library_running = False
                        self.main_menu()
                    if event.ui_element == new_button:
                        new_text = True
                        text_window.set_text("")
                        text_entry.set_text("")
                    if (
                            event.ui_element == save_button
                            and len(text_entry.get_text()) != 0
                    ):
                        if not new_text:
                            changeid = text_select.selected_option
                            changelength = len(text_entry.get_text())
                            query = f"UPDATE text SET passage = '{add_apostrophes(str(text_entry.get_text()))}' WHERE id = {changeid}"
                            self.execute_query(query)
                            # print(changeid, self.keydict)
                            text_window.set_text(self.keydict[changeid])
                            char_window.set_text(str(changelength))
                        else:
                            new_text = False
                            newkeyvalue = len(self.get_keys()) + 1
                            newpassage = text_entry.get_text()
                            query = f"INSERT INTO text (id, passage) VALUES ('{newkeyvalue}', '{add_apostrophes(str(newpassage))}')"
                            self.execute_query(query)
                            self.get_keys()
                            # print(f"key values: {self.keys}")
                            # print(self.keydict)
                            text_select = pygame_gui.elements.UIDropDownMenu(
                                options_list=self.get_keys(),
                                starting_option=f"{newkeyvalue}",
                                relative_rect=pygame.Rect((375, 510), (145, 38)),
                                manager=library_manager,
                                object_id="text_select",
                            )
                            text_window.set_text(self.keydict[str(newkeyvalue)])
                        popupwindow = pygame_gui.windows.UIMessageWindow(
                            rect=pygame.Rect((520, 300), (250, 175)),
                            html_message="passage saved",
                            manager=library_manager,
                        )
                    if event.ui_element == play_button:
                        text = self.keydict[text_select.selected_option]
                        self.play(text)
                        library_running = False
                if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    text_window.set_text(self.keydict[event.text])
                    char_window.set_text(f"{len(self.keydict[event.text])}")
                    text_entry.set_text(self.keydict[event.text])
                library_manager.process_events(event)
            library_manager.update(self.time_delta)
            self.window_surface.blit(manage_library_title, manage_library_title_rect)
            library_manager.draw_ui(self.window_surface)
            pygame.display.flip()


if __name__ == "__main__":
    tm = TypeMaster()
    tm.main_menu()
