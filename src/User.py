class User(object):
    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.name, self.email)