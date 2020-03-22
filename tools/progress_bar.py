from alive_progress import alive_bar, SPINNERS, BARS

def progress_bar_all_chapter(list_chapter, site, directory):
    with alive_bar(len(list_chapter), bar='solid', spinner='classic', calibrate=5) as bar:
        page, number = site.InfoOneChapter(list_chapter[0])
        bar(text=("Downloading Chapter " + number), incr=0)
        for one_chapter in list_chapter:
            page, number = site.InfoOneChapter(one_chapter)
            error_list = site.getOneChapter(page, (directory + "Chapter " + number + "\\"))
            if (error_list != []):
                print(colored(("Error page"+ ', '.join(error_list)), "red"))
            bar(text=("Downloading Chapter " + number))

#def progress_bar_one_chapter(list_chapter, site, directory):