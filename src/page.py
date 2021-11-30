# import tkinter as tk
# from typing import Dict, Callable


# class Page(tk.Tk):
#     """Gui main page where user can control the servos and start scanning
#     """

#     def __init__(self, *args,  **kwargs) -> None:
#         """__init__ initialize a GUI Page with tile, starting and minimal size, and fields that are shown
#         """
#         # __init__ function for class Tk
#         tk.Tk.__init__(self, *args, **kwargs)
#         # self._root: tk.Tk = tk.Tk(className=' Mapping of Disaster Environment')
#         # self._root.minsize(700, 500)    # set the minimal size to "700x500"
#         # self._root.geometry("700x500")  # set the starting window size to "700x500"
#         self.root: tk.Tk = tk.Tk(className=' Mapping of Disaster Environment')
#         self.root.minsize(700, 500)    # set the minimal size to "700x500"
#         self.root.geometry("700x500")  # set the starting window size to "700x500"
#         self._fields: tuple = ("Horizontal", "Vertical")
#         self.entry_string_var: Dict[str, tk.StringVar] = {
#             "Horizontal": tk.StringVar(),
#             "Vertical": tk.StringVar()
#         }

#     def make_form(self) -> None:
#         """make a form to allow user to input horizontal and/or vertical so that the motors will change their position
#         accordingly
#         """
#         servo_rows: Dict[str, tk.Frame] = {}
#         for field in self._fields:
#             servo_row = tk.Frame(self.root,
#                                  width=50,
#                                  height=50)
#             label: tk.Label = tk.Label(servo_row,
#                                        width=8,
#                                        text=field + ": ",
#                                        anchor='w')
#             entry: tk.Entry = tk.Entry(servo_row,
#                                        width=7,
#                                        textvariable=self.entry_string_var[field],
#                                        justify=tk.RIGHT)
#             label.pack(side=tk.LEFT)
#             entry.pack(side=tk.LEFT,
#                        fill=tk.X)
#             servo_rows[field]: tk.Frame = servo_row

#         # position the two frames for "Horizontal" and "Vertical"
#         servo_rows["Horizontal"].place(relx=0.05,
#                                        rely=0.3)
#         servo_rows["Vertical"].place(relx=0.05,
#                                      rely=0.4)

#     def draw_move_button(self, callback: Callable[[Dict[str, tk.StringVar]], None]) -> None:
#         """draw a button for move and associate the callback so that when it is clicked the angles in the entry boxes
#         will be transferred

#         Parameters
#         ----------
#         callback : Callable[[Dict[str, tk.StringVar]], None]
#             the callback function which will take the values in the entry boxes as arguments
#         """
#         button = tk.Button(self.root,
#                            width=7,
#                            bd=4,
#                            text='Move',
#                            command=lambda: callback(self.entry_string_var))
#         button.place(relx=0.1,
#                      rely=0.52)

#     def draw_reset_button(self, callback: Callable[[Dict[str, tk.StringVar]], None]) -> None:
#         """draw a button for reset and associate the callback so that when it is clicked the angles in the entry boxes
#         will be replaced by reset values

#         Parameters
#         ----------
#         callback : Callable[[Dict[str, tk.StringVar]], None]
#             the callback function which will enable values reset
#         """
#         button = tk.Button(self.root,
#                            width=7,
#                            bd=4,
#                            text='Reset',
#                            command=lambda: callback(self.entry_string_var))
#         button.place(relx=0.1,
#                      rely=0.6)

#     def draw_frame_mapping(self) -> None:
#         """draw the frame at a position for the room mapping visualization later on
#         """
#         frame: tk.Frame = tk.Frame(self.root,
#                                    bg="blue")
#         frame.place(relheight=1.0,
#                     relwidth=0.7,
#                     relx=0.3,
#                     rely=0.0)
