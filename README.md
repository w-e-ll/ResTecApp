About
=====

ResTecApp | Development task
----------------------------

ResTecApp is a python3 webapp which groups people living at identical addresses. The
webapp provides two ways to input the data – by manual text entry through a UI
and by uploading а .csv file.
The results are be displayed on the UI and users have an option to download
the results as a .txt file.

Input:
------

1. A file upload input for a utf-8 encoded .csv file with two columns Name,Address.
2. A direct text input on the UI

Output:
-------
1. A text document where each line is a comma-separated list of names of people living at the same address. 
2. The names on each line should be sorted alphabetically. The lines of the file should also be sorted alphabetically.
3. A visualization of the result in the UI


Example input file data:
------------------------
    Name,Address
    Ivan Draganov,”ul. Shipka 34, 1000 Sofia, Bulgaria”
    Leon Wu,”1 Guanghua Road, Beijing, China 100020”
    Ilona Ilieva,”ул. Шипка 34, София, България”
    Dragan Doichinov,”Shipka Street 34, Sofia, Bulgaria”
    Li Deng,”1 Guanghua Road, Chaoyang District, Beijing, P.R.C 100020”
    Frieda Müller,”Konrad-Adenauer-Straße 7, 60313 Frankfurt am Main, Germany”

Expected Output
---------------
    Dragan Doichinov, Ilona Ilieva, Ivan Draganov
    Frieda Müller
    Leon Wu, Li Deng


Project layout
--------------

Here's the directory structure of the ResTecApp project::
    
    test_task
        ├── static
        │     ├── style.css
        ├── templates
        │     ├── 500.html
        │     ├── index.html
        │     ├── validation.html
        ├── tests
        │     └── resourses
        │            ├── ResTecDevTask-sample_input_v1.csv
        │            ├── test.txt
        │
        ├── .gitignore
        ├── app.log
        ├── group.py
        ├── main.py
        ├── README.md       
        └── requirements.txt

Installation
------------
   
    - Made on Linux. Python3.10
    $ 1. git clone https://github.com/w-e-ll/ResTecApp.git
    $ 2. cd ResTecApp 
    $ 3 pip install --upgrade pip
    $ 4. python3 -m venv venv          (Unix/macOS) 
    $ 4. py -m venv venv               (Windows)
    $ 5. source .venv/bin/activate --> (Unix/macOS)
    $ 5. venv\Scripts\activate     --> (Windows)
    $ 6. pip install -r requirements.txt


Usage
-----
    
    $ pytest 
    $ coverage run -m pytest
    $ coverage report -m
    $ python main.py run
    $ http://127.0.0.1:5000/

    P.S. I have provided encoding='utf-8-sig' in main.py line 45 because of Windows file encoding. 
         For me it breaks. So if you will have problems try to change to encoding='utf-8'!
