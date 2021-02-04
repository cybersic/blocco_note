import PySimpleGUIQt as sg
import platform
import os


class Main:
    """
    Main class
    """
    namefile = ""
    mytext = ""
    path = ""
    dw = 1                  #Dark or White

    def path_func(path):
        """
        give the current path
        """

        layout = [
            [sg.Text("Write here the current path")],
            [sg.Input(size=(30, 1), key="-INPUT-" ,change_submits=True), sg.FolderBrowse(key="-IN2-"), sg.Button('Submit')]
        ]

        path_window = sg.Window(
                                'Path',
                                layout,
                                size=(230, 100),
                                no_titlebar=False
                            )

        while True:
            event, tmp_path = path_window.read()

            if event == sg.WIN_CLOSED:
                Main.path = os.path.expanduser("~") + "/"
                break

            if event == 'Submit':
                Main.path = tmp_path.get('-INPUT-') + "/"                   #DA SISTEMARE METTE None IN Main.path
                break

        path_window.close()

        return Main.path

    def namefile_func(namefile):
        """
        give the name of the file
        """

        layout = [
            [sg.Text("Write here the name of the file")],
            [sg.Input(size=(50,1), key='-INPUT-'), sg.Button('Submit')],
            [sg.Output(size=(60,1), key='-OUTP-')]
        ]

        namefile_window = sg.Window(
                                    'Name of the file',
                                    layout,
                                    size=(230, 100),
                                    no_titlebar=False
                                )

        while True:
            event_namefile, namefile_input = namefile_window.read()

            if event_namefile == sg.WIN_CLOSED:
                Main.namefile = Main.path + "nuovo.txt"
                break

            if event_namefile == 'Submit':
                Main.namefile = Main.path + namefile_input.get('-INPUT-')      #extract namefile from dict

                if os.path.exists(Main.namefile) == True:           #check existence of file
                    namefile_window['-OUTP-'].update("The file is already exist, if you want to open use the button Open")
                    continue
                else:
                    f = open(Main.namefile, "a")
                    f.close()
                    break

        namefile_window.close()

        return Main.namefile


    def main_func():
        """
        Main function
        """

        sg.theme('Dark')

        frame1 = [
            [sg.Button('Set the Path'), sg.Button('Save'), sg.Button('Save as'), sg.Button('Open'), sg.Button('Search'), sg.Button("Open terminal"), sg.Output(size=(60,3), key='-OUT-'), sg.Stretch()],
        ]

        frame2 = [
            [sg.Multiline(size=(90,20), key='-INPUT-'), sg.Output(size=(20,20), key='-OUTPUT-'), sg.Stretch()],
        ]

        frame3 = [
            [sg.Button('Save and Quit'), sg.Button('Quit'), sg.Stretch()] #add sg.Button('Dark/White'), for dark or white mode
        ]


        layout = [
                [sg.Frame('', frame1, sg.Stretch())],
                [sg.Frame('', frame2), sg.Stretch(size=(180,90))],
                [sg.Frame('', frame3), sg.Stretch()]
        ]

        main_window = sg.Window('Homepage',                                      #starting main window
                                layout,
                                font=('Arial', 12),
                                return_keyboard_events=True,
                                resizable=True,
                                no_titlebar=False)
                                                                            #DA SISTEMARE SHORTCUT
                                                                            #DA SISTEMARE RESIZABLE

        counter = 0         #for start path window only first time
        while True:
            mytext = {"":""}                                            #initialization of mytext (if you don't write nothing you not have problem when you close)
            if counter > 0:
                files_in_path = ""
                for file in os.listdir(Main.path):
                    files_in_path = files_in_path + file + "\n"

                main_window['-OUTPUT-'].update(files_in_path)  #window files in current path

                main_window['-OUT-'].update("Path: " + Main.path + "\n" + "File: " + Main.namefile)             #window current path and current file

            event_main, mytext = main_window.read(timeout=1)                      #take the data from the main_window

            print(event_main)                   #test

            #quit section
            if event_main == sg.WIN_CLOSED:
                break

            if event_main == 'Quit' or event_main == 'q:24':              #quit
                esc = 0
                layout = [
                    [sg.Text("Are you sure? If you haven't saved your work you will lost all")],
                    [sg.Button('Y'), sg.Button('N')]
                ]

                quit_window = sg.Window('Quitting page', layout, no_titlebar=False)            #quitting page (y/n)

                while True:
                    event_quit, null = quit_window.read()

                    if event_quit == 'N':
                        esc = 0
                    else:
                        esc = 1

                    break

                quit_window.close()

                if esc == 1:
                    break
                else:
                    if esc == 0:
                        continue


            if counter < 1:
                Main.path_func(Main.path)                                    #starting path window (only first time)
                counter += 1


            Main.mytext = mytext.get('-INPUT-')                      #extract text from dict obtained by input


            #operation section
            if event_main == 'Dark/White':                      #change to dark or white mode theme
                if Main.dw == 0:
                    sg.theme('Dark')
                    dw = 1
                elif Main.dw == 1:
                    sg.theme('SystemDefault')
                    dw = 0

            if event_main == 'Set the Path' or event_main == 'k:45':
                Main.path_func(Main.path)                                    #starting path window

            if event_main == 'Save' or event_main == 's:39':
                if Main.namefile == "":
                    Main.namefile_func(Main.namefile)
                Write_read.write(Main.mytext, Main.namefile)             #write on file

            if event_main == 'Save as':
                Main.namefile_func(Main.namefile)
                Write_read.write(Main.mytext, Main.namefile)             #write on file

            if event_main == 'Save and Quit':
                if Main.namefile == "":
                    Main.namefile_func(Main.namefile)

                Write_read.write(Main.mytext, Main.namefile)              #write on file and quit
                break

            if event_main == 'Open' or event_main == 'i:31':
                layout = [
                    [sg.T("")],
                    [sg.Text("Choose a file: "), sg.Input(key="-INP-", change_submits=True), sg.FileBrowse(initial_folder=Main.path, key='-INP2-')],
                    [sg.Button("Submit"), sg.Button("Quit")]
                ]

                open_window = sg.Window('Open file', layout, no_titlebar=False)

                while True:                                         #browsing the file
                    event, to_open = open_window.read()
                    
                    if event == 'Quit' or event_main == 'q:24' or event_main == sg.WIN_CLOSED:
                        break

                    if event == "Submit":
                        to_open = to_open.get('-INP-')
                        Main.namefile = to_open
                        a = open(to_open, "r")
                        main_window['-INPUT-'].update(a.read())                              #go to open page
                        a.close()
                        break
                open_window.close()

            if event_main == 'Search' or event_main == 'f:41':
                Search_class.main_search_func()                           #go to search page

            if event_main == 'Open terminal' or event_main == 't:45':                                #open terminal
                if Main.path == "":                      #if Main.path doesn't exist create it for open the terminal
                    Main.path_func(Main.path)

                if platform.system() == "Windows":                          #choose the correct OS
                    terminal_path = "start cmd.exe " + Main.path
                elif platform.system() == "Darwin":
                    terminal_path = "Terminal " + Main.path
                    os.system("Terminal .")
                elif platform.system() == "Linux":
                    terminal_path = "gnome-terminal --working-directory='" + Main.path + "' || Konsole "  + Main.path

                os.system(terminal_path)            #lauch the terminal with the correct path

        main_window.close()

        return Main.mytext


class Write_read(Main):  #Main class inheritance
    """
    Write and read class
    """
    def read(namefile):
        """
        read from file
        """
        f = open(namefile, "r")

        return f.read()


    def write(mytext, namefile):
        """
        write in file (append)
        """
        f = open(namefile, "w")
        return f.write(mytext)


class Search_class(Main):  #Main class inheritance
    """
    search page class
    """
    #var
    tag = ""                                    #stringa cercata
    row = 0                                     #row of the word searched
    word = ""                                   #word compariser
    file_riga = ""                              #string with file + row


    def search_local_file(file_riga):
        """
        search in local file
        """

        if Main.namefile == "":                                                                    #insert namefile if not defined
            layout = [
                [sg.Text("Write here the name of the file")],
                [sg.Input(size=(50,20), key='-INPU-'), sg.Button('Submit')]
            ]

            namefile_window = sg.Window('Name of the file', layout, no_titlebar=False)

            while True:
                event_namefile, namefile_input = namefile_window.read()

                if event_namefile == 'Submit':
                    Main.namefile = Main.path + namefile_input.get('-INPU-')      #extract namefile from dict
                    f = open(Main.namefile, "a")
                    f.close()
                    break

            namefile_window.close()


        f = open(Main.namefile, "r")
        Search_class.row = 0
        for line in f:
            Search_class.row += 1
            for Search_class.word in line.split(" "):
                if Search_class.tag == Search_class.word:
                    Search_class.row = str(Search_class.row)
                    Search_class.file_riga = "File:" + Main.namefile + " Row:" + Search_class.row
        f.close()

        return Search_class.file_riga


    def search_all_file(file_riga):
        """
        search in all file
        """
        all_file = []
        key = 0

        controller_1 = True
        controller_2 = True

        for file_in_path in os.listdir(Main.path):              #insert in a dict all file in current path
           if os.path.isfile(os.path.join(Main.path, file_in_path)):
               all_file.append(file_in_path)

        while controller_1 == True:
            actual_file = Main.path + all_file[key]               #change of actual_file

            d = open(actual_file, "r")

            Search_class.row = 0
            for line in d:
                Search_class.row += 1
                for word in line.split(" "):
                    if Search_class.tag == word:
                        Search_class.file_riga = "File:" + actual_file + " Row:" + Search_class.row
                        controller_1 = False
            d.close()

            key += 1                                            #update the key to access list of file

        return Search_class.file_riga


    def main_search_func():
        """
        main func search
        """
        layout = [
            [sg.Text("Search the tag here")],
            [sg.Input(size=(70,30), key='-INPUT-')],
            [sg.Output(size=(70,1), key='-OUTPUT_SEARCH-')],
            [sg.Button('Search in file'), sg.Button('Search in all the file'), sg.Button('Quit')]
        ]

        window_search = sg.Window('Search page', layout, no_titlebar=False)

        while True:
            event, tag_input = window_search.read()

            Search_class.tag = tag_input.get('-INPUT-')

            if event == 'Search in file':
                Search_class.tag = tag_input.get('-INPUT-')               #take the searched string from input
                Search_class.search_local_file(Search_class.file_riga)                            #search in local file

            if event == 'Search in all the file':
                Search_class.search_all_file(Search_class.file_riga)

            if event == 'Quit' or event == sg.WIN_CLOSED:
                break

            [window_search['-OUTPUT_SEARCH-'].update(Search_class.file_riga)]                        #update in search_window

        window_search.close()

        return Search_class.file_riga


if __name__ == "__main__":
    Main.main_func()