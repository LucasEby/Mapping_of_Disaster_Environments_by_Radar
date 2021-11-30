# import tkinter as tk
# from typing import Dict
# from multiprocessing import Queue, Process
# from threading import Thread

# from page import Page

# class PageControlProcess(Thread):
#     """PageControl provides control over GUI and communication with servos
#     """
#     def __init__(self, queue: Queue) -> None:
#         """__init__ initialize a page controller takes in both the GUI page and Servos

#         Parameters
#         ----------
#         new_page : Page
#             the GUI page with entry boxes and buttons take user inputs
#         servo : Servos
#             the Servo class which transfer the angles to physical motors
#         """
#         self.__page = Page()
#         self.calls: List[Callable[[str], None]] = []
#         self.queue = queue  # TODO: have changed to see if the multi-processing works
#         #super(PageControlProcess, self).__init__(target=self.start_page)
#         super(PageControlProcess, self).__init__()

#     def start_page(self) -> None:
#         """start the GUI page with labels, entry boxes, and buttons which enables user inputs
#         """
#         self.__page.make_form()
#         self.__page.draw_move_button(self.get_entry_inputs)
#         self.__page.draw_reset_button(self.reset)
#         self.__page.draw_frame_mapping()
#         print("here in gui")
#         self.__page.mainloop()

#     def get_entry_inputs(self, entries: Dict[str, tk.StringVar]) -> None:
#         """get the inputs from the entry boxes which is typed in by the user and pass them to Servos

#         Parameters
#         ----------
#         entries : Dict[str, tk.StringVar]
#             the dictionary has key representing horizontal or vertical angle and their corresponding StringVar objects
#             as values to get the numbers inputted by user
#         """
#         servo_h: str = "h" + entries["Horizontal"].get()
#         servo_v: str = "v" + entries["Vertical"].get()
#         cmd = servo_h + " " + servo_v
#         print("get_entry_inputs outside if")
#         if self.queue.empty():
#             print("get_entry_inputs inside if")
#             self.queue.put(cmd)
#         entries["Horizontal"].set(entries["Horizontal"].get())
#         entries["Vertical"].set(entries["Vertical"].get())

#     def reset(self, entries: Dict[str, tk.StringVar]) -> None:
#         """get the inputs from the entry boxes for reset and pass them to Servos

#         Parameters
#         ----------
#         entries : Dict[str, tk.StringVar]
#             the dictionary has key representing horizontal or vertical angle and their corresponding StringVar objects
#             as values so that reset angles can be put into the entry boxes
#         """
#         servo_h: str = "h100"
#         servo_v: str = "v180"
#         cmd = servo_h + " " + servo_v
#         if self.queue.empty():
#             self.queue.put(cmd)
#         entries["Horizontal"].set("100")
#         entries["Vertical"].set("180")

#     def run(self):
#         self.start_page()
