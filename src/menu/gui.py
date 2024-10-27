import PyQt6
import PyQt6.QtWidgets
import PyQt6.QtGui
import PyQt6.QtCore

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

sh.gi.ICON = sh.objs.get_pdir().add('..', 'resources', 'unmusic.png')


class Menu:
    
    def __init__(self, *args, **kwargs):
        self.set_gui()
    
    def minimize(self):
        self.window.showMinimized()
    
    def centralize(self):
        ''' Do this only after showing the widget; otherwise, it will have
            bogus dimensions of 640×480.
        '''
        self.app.move(sh.objs.get_root().primaryScreen().geometry().center() - self.app.rect().center())
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            PyQt6.QtGui.QShortcut(PyQt6.QtGui.QKeySequence(hotkey), self.window).activated.connect(action)
    
    def set_buttons(self):
        self.btn_edt = sh.Button (_('Album Editor'))
        self.btn_prp = sh.Button (text = _('Prepare files')
                                 ,hint = _('Move sub-folders to a root folder, split large lossless files, etc.')
                                 )
        self.btn_col = sh.Button(_('Collect tags & Obfuscate'))
        self.btn_cop = sh.Button(_('Copy music'))
        self.btn_del = sh.Button(_('Delete low-rated music'))
        self.btn_qit = sh.Button(_('Quit'))
    
    def add_buttons(self):
        self.layout.addWidget(self.btn_edt.widget)
        self.layout.addWidget(self.btn_prp.widget)
        self.layout.addWidget(self.btn_col.widget)
        self.layout.addWidget(self.btn_cop.widget)
        self.layout.addWidget(self.btn_del.widget)
        self.layout.addWidget(self.btn_qit.widget)
    
    def set_layout(self):
        self.app = PyQt6.QtWidgets.QMainWindow()
        self.window = PyQt6.QtWidgets.QWidget()
        self.layout = PyQt6.QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.window.setLayout(self.layout)
        self.app.setCentralWidget(self.window)
    
    def set_icon(self):
        # Does not accept None
        self.window.setWindowIcon(sh.gi.objs.get_icon())
    
    def set_title(self, title='unmusic'):
        self.window.setWindowTitle(title)
    
    def configure(self):
        self.btn_edt.set_default()
        self.btn_edt.change_font_size(2)
        self.btn_prp.change_font_size(2)
        self.btn_col.change_font_size(2)
        self.btn_cop.change_font_size(2)
        self.btn_del.change_font_size(2)
        self.btn_qit.change_font_size(2)
    
    def set_gui(self):
        self.set_layout()
        self.set_buttons()
        self.add_buttons()
        self.set_icon()
        self.set_title()
        self.configure()
    
    def show(self):
        self.app.show()
    
    def close(self):
        self.app.close()
