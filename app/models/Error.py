class IssueError:
    def __init__(self, code, message):
        self.error = True
        self.code = code
        self.message = message
        
    def to_json(self):
        return {
            'error': self.error,
            'code': self.code,
            'message': self.message,
        }
        