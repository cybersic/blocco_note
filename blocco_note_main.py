import PySimpleGUI as sg
import platform
import os


class Main:
    """
    Main class
    """
    namefile = ""
    mytext = ""
    path = ""

    def path_func(path):
        """
        give the current path
        """

        layout = [
            [sg.Text("Write here the current path")],
            [sg.FolderBrowse(key="-INPUT-"), sg.Button('Ok')]
        ]

        path_window = sg.Window('Path', layout, size=(230, 100))

        while True:
            event, path = path_window.read()

            if event == sg.WINDOW_CLOSED:
                break
            elif event == 'Ok':
                Main.path = path.get('-INPUT-') + "/"
                break

        path_window.close()

        sg.WINDOW_CLOSED = False

        return Main.path

    def namefile_func(namefile):
        """
        give the name of the file
        """

        layout = [
            [sg.Text("Write here the name of the file")],
            [sg.Input(size=(50,20), key='-INPUT-'), sg.Button('Submit')]
        ]

        namefile_window = sg.Window('Name of the file', layout)

        while True:
            event_namefile, namefile = namefile_window.read()

            if event_namefile == sg.WINDOW_CLOSED:
                break
            elif event_namefile == 'Submit':
                #DA SISTEMARE: FAI CONTROLLO ESISTENZA FILE PER EVITARE SOVRASCRITTURA
                f = open(namefile.get('-INPUT-'), "a")
                f.close()
                Main.namefile = Main.path + namefile.get('-INPUT-')
                break

        namefile_window.close()

        sg.WINDOW_CLOSED = False

        return Main.namefile


    def main_func():
        """
        Main function
        """

        sg.theme('DarkBlue12')

        layout = [
            [sg.Text("Write here")],
            [sg.Button('Save'), sg.Button('Save as'), sg.Button('Open'), sg.Button('Search'), sg.Button("Open terminal"), sg.Output(size=(100,4), key='-OUT-')],
            [sg.Multiline(size=(130,50), key='-INPUT-'), sg.Output(size=(25,50), key='-OUTPUT-')],
            [sg.Button('Save and Quit'), sg.Button('Quit')]
        ]

        main_window = sg.Window('Homepage', layout)              #starting main window

        counter = 0         #for start path window only first time
        while True:
            if counter > 0:
                main_window['-OUTPUT-'].update(os.listdir(Main.path))  #finestra current path con file presenti in current folder
                                                                       #DA SISTEMARE OUTPUT (non va a capo)
                main_window['-OUT-'].update("Path: " + Main.path + "\n" + "File: " + Main.namefile)                 #mostra path e file nella finestra -OUT-

            event_main, mytext = main_window.read()                      #take the data from the main_window

            if counter < 1:
                Main.path_func(Main.path)                                    #starting path window
                counter += 1


            Main.mytext = mytext.get('-INPUT-')                      #extract text from dict obtained by input

            #operation section

            if event_main == 'Save':
                if Main.namefile == "":
                    Main.namefile_func(Main.namefile)
                Write_read.write(Main.mytext, Main.namefile)             #write on file

            if event_main == 'Save as':
                Main.namefile_func(Main.namefile)
                Write_read.write(Main.mytext, Main.namefile)             #write on file

            if event_main == 'Open':
                layout = [[sg.T("")], [sg.Text("Choose a file: "), sg.Input(key='-INP-'), sg.FileBrowse(initial_folder=Main.path, key='-INP-')],[sg.Button("Submit")]]

                open_window = sg.Window('My File Browser', layout, size=(600,150))

                while True:                                         #browsing the file
                    event, to_open = open_window.read()
                    if event == sg.WIN_CLOSED or event=="Exit":
                        break
                    elif event == "Submit":
                        to_open = to_open.get('-INP-')
                        Main.namefile = to_open
                        a = open(to_open, "r")
                        main_window['-INPUT-'].update(a.read())                              #go to open page
                        a.close()
                        break
                open_window.close()

            if event_main == 'Search':
                Search_class.main_search_func()                           #go to search page            DA SISTEMARE

            if event_main == 'Open terminal':                                #open terminal
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


            #quit section

            if event_main == 'Save and Quit':
                if Main.namefile == "":
                    Main.namefile_func(Main.namefile)

                Write_read.write(Main.mytext, Main.namefile)              #write on file and quit
                break

            if event_main == 'Quit' or event_main == sg.WINDOW_CLOSED:              #quit
                esc = 0
                layout = [
                    [sg.Text("Are you sure? If you haven't saved your work you will lost all")],
                    [sg.Button('Y'), sg.Button('N')]
                ]

                quit_window = sg.Window('Quitting page', layout)            #quitting page (y/n)

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


        main_window.close()

        return Main.mytext


class Write_read(Main):
    """
    Write and read class, inheritance by main
    """
    row = 0

    word = ""
    all_word = {}

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


class Search_class(Write_read):  #Main class is ereditary by Write_read, multilevel inerhitance
    """
    search page class
    """
    searched_string = ""                        #stringa cercata
    file_riga = ()                              #tupla con nome del file e riga della stringa cercata

    def search_local_file(file_riga):
        """
        search in local file
        """

        if Main.namefile == "":
            Main.namefile_func(Main.namefile)                                                   #inserisci namefile se assente

        f = open(Main.namefile, "r")
        for line in f:
            Write_read.row += 1
            for Write_read.word in line.split(" "):
                Write_read.all_word[Write_read.row] = Write_read.word           #put the word in a dictionary with correct row as key


        exit_var = 1
        while True:
            if exit_var == 0:
                break
            print("parola cercata", Search_class.searched_string, type(Search_class.searched_string))                     #test
            print("parola da cercare nel dict", Write_read.word, type(Write_read.word))                                   #test
            print("parole nel dict", Write_read.all_word, type(Write_read.all_word))                                      #test

            for Write_read.word in Write_read.all_word.values():
                print("parola", Write_read.word)                                                                          #test
                if Search_class.searched_string + "\n" == Write_read.word:     #SISTEMA READ (CRASH SE PAROLE IN STESSA RIGA)
                    Search_class.file_riga = (Main.namefile, Write_read.row)

                    print("file e riga:", Search_class.file_riga)                                                         #test

                    Search_class.searched_string = ""                   #SISTEMA FLUSH DELLE VARIABILI
                    Write_read.all_word = {}
                    Write_read.word = ""

                    exit_var = 0
                    break

        return Search_class.file_riga


    def search_all_file(file_riga):
        """
        search in all file
        """
        return Search_class.file_riga


    def main_search_func():
        """
        main func search
        """
        layout = [
            [sg.Text("Search here")],
            [sg.Input(size=(70,30), key='-INPUT-')],
            [sg.Text(size=(15,1), key='-OUTPUT-')],
            [sg.Button('Search in file'), sg.Button('Search in all the file'), sg.Button('Quit')]
        ]

        window_search = sg.Window('Search page', layout)

        while True:
            event, searched_string_input = window_search.read()

            Search_class.searched_string = searched_string_input.get('-INPUT-')

            if event == 'Search in file':
                Search_class.searched_string = searched_string_input.get('-INPUT-')               #take the searched string from input
                Search_class.search_local_file(Search_class.file_riga)                            #search in local file
                print(Search_class.file_riga)                                   #test
                [window_search['-OUTPUT-'].update(Search_class.file_riga)]                        #update in search_window

            if event == 'Search in all the file':
                Search_class.search_all_file(Search_class.file_riga)

            if event == sg.WINDOW_CLOSED or event == 'Quit':
                break

        window_search.close()

        return Search_class.file_riga


if __name__ == "__main__":
    Main.main_func()