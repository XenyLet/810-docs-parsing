### найденные баги

1. Запуск на директории с одним файлом
```
Traceback (most recent call last):
  File "/media/apps/jetbrains/pycharm-community-2022.2.2/plugins/python-ce/helpers/pydev/pydevd.py", line 1496, in _exec
    pydev_imports.execfile(file, globals, locals)  # execute the script
  File "/media/apps/jetbrains/pycharm-community-2022.2.2/plugins/python-ce/helpers/pydev/_pydev_imps/_pydev_execfile.py", line 18, in execfile
    exec(compile(contents+"\n", file, 'exec'), glob, loc)
  File "/media/projects/ks/810-docs-parsing/easy_way/main.py", line 10, in <module>
    main()
  File "/media/projects/ks/810-docs-parsing/easy_way/main.py", line 6, in main
    elems, unrecognized_list = recognizing(path_to_pdf)
  File "/media/projects/ks/810-docs-parsing/easy_way/recognize.py", line 13, in recognizing
    list_of_elements, specification, other, img_list_of_elems, img_specification = create_list_of_pdf(path_to_pdf)
  File "/media/projects/ks/810-docs-parsing/easy_way/search_pdf.py", line 45, in create_list_of_pdf
    return list_of_elements, specification, other, img_list_of_elems, img_specification
UnboundLocalError: local variable 'img_specification' referenced before assignment
python-BaseException
Backend TkAgg is interactive backend. Turning interactive mode on.
```
Переменные не были проинициализированы пустыми значениями

2. после правки ошибки выше

```
Traceback (most recent call last):
  File "/media/apps/jetbrains/pycharm-community-2022.2.2/plugins/python-ce/helpers/pydev/pydevd.py", line 1496, in _exec
    pydev_imports.execfile(file, globals, locals)  # execute the script
  File "/media/apps/jetbrains/pycharm-community-2022.2.2/plugins/python-ce/helpers/pydev/_pydev_imps/_pydev_execfile.py", line 18, in execfile
    exec(compile(contents+"\n", file, 'exec'), glob, loc)
  File "/media/projects/ks/810-docs-parsing/easy_way/main.py", line 10, in <module>
    main()
  File "/media/projects/ks/810-docs-parsing/easy_way/main.py", line 6, in main
    elems, unrecognized_list = recognizing(path_to_pdf)
  File "/media/projects/ks/810-docs-parsing/easy_way/recognize.py", line 62, in recognizing
    for elem in img_matrix[0]:
IndexError: list index out of range
```

Были перепутаны переменные для итерации


3. 



