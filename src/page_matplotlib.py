import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
from multiprocessing import Process, Queue


class PageMatplotlib(Process):
    """Gui main page where user can control the servos and start scanning
    """
    h_angle = 100
    v_angle = 180

    def __init__(self, queue: Queue) -> None:
        """__init__ initialize a GUI Page with tile, starting and minimal size, and fields that are shown
        """
        self.queue = queue
        self.target = self.show_page
        super(PageMatplotlib, self).__init__(target=self.show_page)

    def  show_page(self):
        self.fig = plt.figure()

        self.ax_box_horizontal = plt.axes([0.4, 0.66, 0.1, 0.075])
        self.text_box_horizontal = TextBox( self.ax_box_horizontal, 'Horizontal: ', initial="100")
        self.text_box_horizontal.on_submit(self.get_horizontal)
    
        self.ax_box_vertical = plt.axes([0.4, 0.55, 0.1, 0.075])
        self.text_box_vertical = TextBox(self.ax_box_vertical, 'Vertical: ', initial="180")
        self.text_box_vertical.on_submit(self.get_vertical)
        
        self.ax_b_move = plt.axes([0.4, 0.44, 0.1, 0.075])
        self.b_move = Button(self.ax_b_move, 'Move')
        self.b_move.on_clicked(self.move)
        
        self.ax_b_reset = plt.axes([0.4, 0.33, 0.1, 0.075])
        self.b_reset = Button(self.ax_b_reset, 'Reset')
        self.b_reset.on_clicked(self.reset)

        self.ax_b_complete_rotate = plt.axes([0.4, 0.22, 0.2, 0.075])
        self.b_complete_rotate = Button(self.ax_b_complete_rotate, 'Complete Scan')
        self.b_complete_rotate.on_clicked(self.complete_rotate)
        
        plt.show()
        plt.pause(0.01)

    def get_horizontal(self, angle):
        self.h_angle = eval(angle)

    def get_vertical(self, angle):
        self.v_angle = eval(angle)

    def move(self, event):
        cmd = "h" + str(self.h_angle) + " v" + str(self.v_angle)
        if self.queue.empty():
            # print("cmd in page_matplotlib: " + cmd)
            self.queue.put(cmd)

    def reset(self, event):
        self.text_box_horizontal.set_val("100")
        self.text_box_vertical.set_val("180")
        cmd = "r r"
        if self.queue.empty():
            self.queue.put(cmd)

    def complete_rotate(self, event):
        cmd = "w r"
        if self.queue.empty():
            self.queue.put(cmd)