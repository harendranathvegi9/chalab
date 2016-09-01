import logging
import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException

log = logging.getLogger('functional.pages')
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())


class SelectableMixin(object):
    @property
    def selectable(self):
        try:
            return self.elem
        except AttributeError:
            return self.driver

    def by_css(self, selector, on_missing=Exception):
        try:
            return self.selectable.find_element_by_css_selector(selector)
        except (NoSuchElementException, TimeoutException) as e:
            if on_missing != Exception:
                return on_missing
            else:
                self.capture("by_css_%s" % selector)
                raise e

    def by_css_many(self, selector, on_missing=Exception, clss=None):
        try:
            xs = self.selectable.find_elements_by_css_selector(selector)
        except (NoSuchElementException, TimeoutException) as e:
            if on_missing != Exception:
                return on_missing
            else:
                raise e

        if clss is not None:
            return [clss(self, x) for x in xs]
        else:
            return xs

    def click(self, selector=None):
        if selector is None:
            self.elem.click()
        else:
            self.by_css(selector).click()


class CapturableMixin(object):
    def capture(self, name):
        name = """./tests/captures/%s_%s_%020d""" % (self.__class__.__name__, name, time.time())
        self.driver.save_screenshot(name + '.png')


class BasicElementsMixin(object):
    selector_content = '.content'

    @property
    def h1(self):
        return self.by_css('h1')

    @property
    def h2(self):
        return self.by_css('h2')

    @property
    def h3(self):
        return self.by_css('h3')

    @property
    def content(self):
        return self.by_css(self.selector_content)


class Block(SelectableMixin, CapturableMixin, BasicElementsMixin):
    selector = None

    def __init__(self, parent):
        assert self.selector is not None, "define a selector for this block."
        self.parent = parent
        self.driver = parent.driver
        self.elem = self.by_css(self.selector)


class FormBlock(Block):
    def has_fields(self, inputs):
        for i in inputs:
            if not self.by_css('input#id_%s' % i, on_missing=False):
                return False

        return True

    def fill(self, **kwargs):
        for (k, v) in kwargs.items():
            try:
                self.by_css('input#id_%s' % k).send_keys(v)
            except (NoSuchElementException, TimeoutException):
                self.by_css('textarea#id_%s' % k).send_keys(v)

        return self

    def submit(self):
        self.elem.submit()
        return self


class HeroBlock(Block):
    selector = '.hero'
    selector_lead = '.lead'

    @property
    def lead(self):
        return self.by_css(self.selector_lead)


class JumbotronBlock(Block):
    selector = '.jumbotron'


class AppMixin(object):
    app, panel = None, None

    def checked(self):
        assert self.app is not None, "forgot to define the AppMixin?"

        try:
            assert self.is_(self.app, self.panel)
        except AssertionError:
            self.capture("""check_%s_%s_%010d""" % (self.app, self.panel, time.time()))

        return self

    def _is_(self, kind, value):
        x = self.by_css('.%s#%s' % (kind, value), on_missing=None) is not None

        if not x:
            m = self.by_css('.%s' % kind)
            log.warning("got %s: %s, expected: %s", kind, m.get_attribute('id'), value)

        return x

    def is_app(self, name):
        return self._is_('app', name)

    def is_panel(self, name):
        return self._is_('panel', name)

    def is_module(self, name):
        return self._is_('module', name)

    def is_(self, app, panel=None):
        return (self.is_app(app) and
                self.is_panel(panel) if panel is not None else True)


class Page(SelectableMixin, CapturableMixin, BasicElementsMixin, AppMixin):
    selector_content = '.content'

    def __init__(self, driver_or_prev):
        try:
            self.driver = driver_or_prev.driver
            self.prev = driver_or_prev
        except AttributeError:
            self.driver = driver_or_prev
            self.prev = None

    def get(self, url):
        self.driver.get(url)
        return self

    @property
    def content(self):
        return self.by_css(self.selector_content)

    @property
    def hero(self):
        return HeroBlock(self)

    @property
    def jumbotron(self):
        return JumbotronBlock(self)

    def nav_to(self, page_name):
        self.by_css('nav #%s a' % page_name).click()
        return self