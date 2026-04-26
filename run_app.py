import sys
print('starting run_app')
try:
    from Registerion_form import RegisterationForm
    print('imported Registerion_form')
    from Student_List import StudentList
    print('imported Student_List')
    from database_handler import DatabaseHandler
    print('imported DatabaseHandler')
    from main import MyApplication
    print('imported MyApplication')
except Exception as e:
    print('import error:', e)
    sys.exit(1)

print('creating app')
app = MyApplication()
print('app created, entering mainloop')
try:
    print('app state:', app.state())
    print('winfo_viewable:', app.winfo_viewable())
    print('children:', app.winfo_children())
except Exception as e:
    print('error querying app state:', e)

app.mainloop()
print('app exited')
