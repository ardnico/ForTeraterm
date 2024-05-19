from ..CTkMessagebox.ctkmessagebox import CTkMessagebox

def show_info(title="Info", message="This is a CTkMessagebox!"):
    # Default messagebox for showing some information
    CTkMessagebox(title=title, message=message)

def show_checkmark(message="CTkMessagebox is successfully installed.",option_1="Thanks"):
    # Show some positive message with the checkmark icon
    CTkMessagebox(message=message, icon="check", option_1=option_1)
    
def show_error(title="Error", message="Something went wrong!!!"):
    # Show some error message
    CTkMessagebox(title=title, message=message, icon="cancel")
    
def show_warning(title="Warning Message!", message="Unable to connect!", option_1="Cancel", option_2="Retry"):
    # Show some retry/cancel warnings
    msg = CTkMessagebox(title=title, message=message, icon="warning", option_1=option_1, option_2=option_2)
    return msg.get()
    
def ask_question(title="Exit?", message="Do you want to close the program?", option_1="Cancel", option_2="No", option_3="Yes"):
    # get yes/no answers
    msg = CTkMessagebox(title=title, message=message, icon="question", option_1=option_1, option_2=option_2, option_3=option_3)
    return msg.get()

