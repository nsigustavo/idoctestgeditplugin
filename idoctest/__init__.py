globs=globals().copy()

import gedit
import gtk
import re
from _utils import stdout_redirected
from StringIO import StringIO
import sys
import traceback
from doctest import DocTestParser


class IDoctestPlugin(gedit.Plugin):
    shift=False

    def __init__(self):
        gedit.Plugin.__init__(self)
        self.window = None
        self.id_name = 'idoctest'

    def activate(self, window):
        """Activate plugin."""
        self.window = window
        for view in window.get_views():
            uid_press = view.connect('key-press-event', self.key_press_event)
            uid_release = view.connect('key-release-event', self.key_release_event)
            view.set_data(self.id_name, [uid_press, uid_release])

    def deactivate(self, window):
        """Deactivate plugin."""
        for view in window.get_views():
            for uid in view.get_data(self.id_name):
                view.disconnect(uid)
            view.set_data(self.id_name, None)
        self.window = None

    def update_ui(self, window):
        self.activate(window)

    def key_release_event(self, view, event):
        key = gtk.gdk.keyval_name(event.keyval)
        if key in ('Shift_L', 'Shift_R'):
            self.shift = False

    def key_press_event(self, view, event):
        key = gtk.gdk.keyval_name(event.keyval)
        if key in ('Shift_L', 'Shift_R'):
            self.shift = True
        if self.shift and key == 'Return':
            self.shift = False
            return self.insertOutOfDocTest()
        elif not self.shift and key == 'Return':
            return self.insertContinuation()

    def insertOutOfDocTest(self):
        fixture, snippet = self.fixture_and_snippet()
        idoctest = IDocTest()
        out_snippet = idoctest.run(fixture, snippet)
        if out_snippet:
            self.doc.insert_at_cursor(out_snippet  + '>>> ')
            return True

    def insertContinuation(self):
        init_snippet, end_snippet = self._textline_bounds()
        line = self.doc.get_text(init_snippet, end_snippet)
        line_match = re.search(r'(?P<indentline> *)(?P<marcador>\>\>\> |\.\.\. )(?P<indentcode> *)(?P<code>.*)', line)
        if line_match:
            indentline, marcador, indentcode, code = line_match.groups()
            if (marcador in ('... ', '>>> ')
            and (line_match.group('code').endswith(':')
            or line_match.group('code').endswith(')'))):
                if line_match.group('code').endswith(':'):
                    indentcode += '    '
                self.doc.insert_at_cursor('\n'+indentline+'... '+indentcode)
                return True

    def fixture_and_snippet(self):
        init_file, end_file = self.doc.get_bounds()
        init_snippet, end_snippet = self._get_snippet_bounds()
        fixture = self.doc.get_text(init_file, init_snippet)
        snippet = self.doc.get_text(init_snippet, end_snippet)
        return fixture, snippet

    def _get_snippet_bounds(self):
        init_snippet, end_snippet = self._textline_bounds()
        while not re.search(r' *>>> ', self.doc.get_text(init_snippet, end_snippet)):
            if not re.search(r' *>>> | *... ', self.doc.get_text(init_snippet, end_snippet)):
                return end_snippet, end_snippet
            init_snippet.backward_line()
        return init_snippet, end_snippet

    def _textline_bounds(self):
        end_line = self.doc.get_iter_at_mark(self.doc.get_insert())
        init_line = end_line.copy()
        init_line.set_line_index(0)
        return init_line, end_line

    @property
    def doc(self):
        return self.window.get_active_document()


class IDocTest:

    parser = DocTestParser()
    filename = '<idoctest gedit plugin: by Gustavo Rezende>'

    def __init__(self):
        self.globs = globs.copy()

    def _gotFormatException(self):
        exc_info = sys.exc_info()
        return ''.join(traceback.format_exception(*exc_info))

    def _execute(self, example):
        newStdout = StringIO()
        with stdout_redirected(newStdout):
            try:
                exec compile(example.source, self.filename, 'single') in self.globs
                output =  newStdout.getvalue()
            except:
                output = self._gotFormatException()
        return output

    def run(self, fixture_text, snippet_text):
        fixture = self.get_steps(fixture_text)
        snippet = self.get_steps(snippet_text)
        self.run_fixture(fixture)
        out_snippet = self.run_snippet(snippet)
        return out_snippet

    def run_snippet(self, snippet_examples):
        if snippet_examples:
            output = self._execute(snippet_examples[0])
            return self.format_with_indent(snippet_examples[0], output)
        return ''

    def run_fixture(self, examples):
        for example in examples:
            self._execute(example)

    def get_steps(self, snippet):
        try:
            return self.parser.get_examples(snippet, name=self.filename)
        except:pass

    def format_with_indent(self, example, out):
        line_init = ' '*(example.indent)
        return "".join(['\n'+line_init+line for line in out.split('\n')])

