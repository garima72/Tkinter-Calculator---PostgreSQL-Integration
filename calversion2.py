import tkinter as tk
import psycopg2

# --- Database Setup ---
# Update these database credentials before running
DB_NAME = "your_database-name"
DB_USER = "your-_sername"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"

def init_db():
    
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS calc_history (
                id SERIAL PRIMARY KEY,
                calculation TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Database connection error: {e}")

def save_to_history(calculation_str):
    
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO calc_history (calculation) VALUES (%s);", (calculation_str,)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Failed to log history: {e}")
init_db()


# --- Tkinter GUI-----
window = tk.Tk()
window.title("Calculator")
window.geometry("400x500")

e = tk.Entry(window, width=45, borderwidth=5)
e.place(x=10, y=10)

n1 = None
math = ""

def click(number):
    current = e.get()
    e.delete(0, tk.END)
    e.insert(0, str(current) + str(number))

def clear():
    e.delete(0, tk.END)

def add():
    global n1
    global math
    first_number = e.get()
    math = "addition"
    n1 = int(first_number)
    e.delete(0, tk.END)

def sub():
    global n1
    global math
    first_number = e.get()
    math = "subtraction"
    n1 = int(first_number)
    e.delete(0, tk.END)

def mult():
    global n1
    global math
    first_number = e.get()
    math = "multiplication"
    n1 = int(first_number)
    e.delete(0, tk.END)

def div():
    global n1
    global math
    first_number = e.get()
    math = "division"
    n1 = int(first_number)
    e.delete(0, tk.END)


def equal():
    global n1
    second_number = e.get()
    e.delete(0, tk.END)
    
    result = None
    operation_symbol = ""
    
    if math == "addition":
        operation_symbol = "+"
        result = n1 + int(second_number)
    elif math == "subtraction":
        operation_symbol = "-"
        result = n1 - int(second_number)
    elif math == "multiplication":
        operation_symbol = "*"
        result = n1 * int(second_number)
    elif math == "division":
        operation_symbol = "/"
        if int(second_number) != 0:
            result = n1 / int(second_number)
        else:
            e.insert(0, "Error")
            return

    if result is not None:
        e.insert(0, result)
        calc_str = f"{n1} {operation_symbol} {second_number} = {result}"
        save_to_history(calc_str)

def show_history():
    history_window = tk.Toplevel(window)
    history_window.title("Calculation History")
    history_window.geometry("350x400")

    listbox = tk.Listbox(history_window, width=50, height=20)
    listbox.pack(padx=10, pady=10, fill="both", expand=True)

    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

        cursor = conn.cursor()

        cursor.execute("""
            SELECT calculation
            FROM calc_history
            ORDER BY id DESC;
        """)

        rows = cursor.fetchall()

        if not rows:
            listbox.insert(tk.END, "No calculation history found.")
        else:
            for row in rows:
                listbox.insert(tk.END, row[0])

        cursor.close()
        conn.close()

    except Exception as e:
        listbox.insert(tk.END, f"Error: {e}")

# --- BUTTONS ---

# Row 1: 1, 2, 3
b1 = tk.Button(window, text='1', width=12, command=lambda: click(1))
b1.place(x=10, y=60)
b2 = tk.Button(window, text='2', width=12, command=lambda: click(2))
b2.place(x=110, y=60)
b3 = tk.Button(window, text='3', width=12, command=lambda: click(3))
b3.place(x=210, y=60)

# Row 2: 4, 5, 6
b4 = tk.Button(window, text='4', width=12, command=lambda: click(4))
b4.place(x=10, y=110)
b5 = tk.Button(window, text='5', width=12, command=lambda: click(5))
b5.place(x=110, y=110)
b6 = tk.Button(window, text='6', width=12, command=lambda: click(6))
b6.place(x=210, y=110)

# Row 3: 7, 8, 9
b7 = tk.Button(window, text='7', width=12, command=lambda: click(7))
b7.place(x=10, y=160)
b8 = tk.Button(window, text='8', width=12, command=lambda: click(8))
b8.place(x=110, y=160)
b9 = tk.Button(window, text='9', width=12, command=lambda: click(9))
b9.place(x=210, y=160)

# Row 4: 0, +, -
b0 = tk.Button(window, text='0', width=12, command=lambda: click(0))
b0.place(x=10, y=210)
b_add = tk.Button(window, text='+', width=12, command=add)
b_add.place(x=110, y=210)
b_sub = tk.Button(window, text='-', width=12, command=sub)
b_sub.place(x=210, y=210)

# Row 5: *, /, =
b_mult = tk.Button(window, text='*', width=12, command=mult)
b_mult.place(x=10, y=260)
b_div = tk.Button(window, text='/', width=12, command=div)
b_div.place(x=110, y=260)
b_equal = tk.Button(window, text='=', width=12, command=equal)
b_equal.place(x=210, y=260)

# Row 6
b_clear = tk.Button(window, text="Clear", width=12, command=clear)
b_clear.place(x=10, y=310)

b_history = tk.Button(window, text="History", width=12, command=show_history)
b_history.place(x=110, y=310)

window.mainloop()