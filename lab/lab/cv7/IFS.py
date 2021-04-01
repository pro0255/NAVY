class IFS:
    def __init__(self):
        pass

    def process(self, m_g):
        print(m_g)
        for _ in range(m_g):
            self.generation()
        return 0, 0, 0

    def generation(self):
        print("g")
