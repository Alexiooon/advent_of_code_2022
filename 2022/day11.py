"""Day 11 challenges."""
# pylint: disable=invalid-name
# Imports
import os

# Read the input data
path = os.path.join('.', 'data', 'day11_monkeys.txt')
with open(path, 'r', encoding='utf8') as f:
    monkey_status = f.read().splitlines()

# %% Challenge 1
class Monkey():
    """An empty husk of a monkey with no rules or morals"""
    def __init__(self, items: list[int]):
        self.items = items

    def bore(self):
        """Monkey gets bored with item."""
        self.items[0] = int(self.items[0] / 3)

    def catch(self, item: int):
        """Catch an item from another monkey"""
        self.items.append(item)

    def inspect(self):
        """Rule regarding worry level"""
        raise NotImplementedError

    def check(self):
        """Check to determine where the monkey will toss his"""
        raise NotImplementedError


class Monkey0(Monkey):
    """Monke #0."""

    def __init__(self) -> None:
        super().__init__([74, 73, 57, 77, 74])
        self._monkey_friends = {True: 6, False: 7}

    def inspect(self):
        """Rule regarding worry level"""
        self.items[0] = self.items[0] * 11

    def check(self):
        """Check to determine where the monkey will toss his"""
        return self._monkey_friends[self.items[0] % 19 == 0], self.items.pop(0)


class Monkey1(Monkey):
    """Monke #1."""

    def __init__(self) -> None:
        super().__init__([99, 77, 79])
        self._monkey_friends = {True: 6, False: 0}

    def inspect(self):
        """Rule regarding worry level"""
        self.items[0] = self.items[0] + 8

    def check(self):
        """Check to determine where the monkey will toss his"""
        return self._monkey_friends[self.items[0] % 2 == 0],  self.items.pop(0)


class Monkey2(Monkey):
    """Monke #2."""

    def __init__(self) -> None:
        super().__init__([64, 67, 50, 96, 89, 82, 82])
        self._monkey_friends = {True: 5, False: 3}

    def inspect(self):
        """Rule regarding worry level"""
        self.items[0] = self.items[0] + 1

    def check(self):
        """Check to determine where the monkey will toss his"""
        return self._monkey_friends[self.items[0] % 3 == 0], self.items.pop(0)


class Monkey3(Monkey):
    """Monke #3."""

    def __init__(self) -> None:
        super().__init__([88])
        self._monkey_friends = {True: 5, False: 4}

    def inspect(self):
        """Rule regarding worry level"""
        self.items[0] = self.items[0] * 7

    def check(self):
        """Check to determine where the monkey will toss his"""
        return self._monkey_friends[self.items[0] % 17 == 0], self.items.pop(0)


class Monkey4(Monkey):
    """Monke #4."""

    def __init__(self) -> None:
        super().__init__([80, 66, 98, 83, 70, 63, 57, 66])
        self._monkey_friends = {True: 0, False: 1}

    def inspect(self):
        """Rule regarding worry level"""
        self.items[0] = self.items[0] + 4

    def check(self):
        """Check to determine where the monkey will toss his"""
        return self._monkey_friends[self.items[0] % 13 == 0], self.items.pop(0)


class Monkey5(Monkey):
    """Monke #5."""

    def __init__(self) -> None:
        super().__init__([81, 93, 90, 61, 62, 64])
        self._monkey_friends = {True: 1, False: 4}

    def inspect(self):
        """Rule regarding worry level"""
        self.items[0] = self.items[0] + 7

    def check(self):
        """Check to determine where the monkey will toss his"""
        return self._monkey_friends[self.items[0] % 7 == 0],  self.items.pop(0)


class Monkey6(Monkey):
    """Monke #6."""

    def __init__(self) -> None:
        super().__init__([69, 97, 88, 93])
        self._monkey_friends = {True: 7, False: 2}

    def inspect(self):
        """Rule regarding worry level"""
        self.items[0] = self.items[0] * self.items[0]

    def check(self):
        """Check to determine where the monkey will toss his"""
        return self._monkey_friends[self.items[0] % 5 == 0], self.items.pop(0)


class Monkey7(Monkey):
    """Monke #7."""

    def __init__(self) -> None:
        super().__init__([59, 80])
        self._monkey_friends = {True: 2, False: 3}

    def inspect(self):
        """Rule regarding worry level"""
        self.items[0] = self.items[0] + 6

    def check(self):
        """Check to determine where the monkey will toss his"""
        return self._monkey_friends[self.items[0] % 11 == 0], self.items.pop(0)


# Do some monkey business
rounds = 20
total_inspections = [0, 0, 0, 0, 0, 0, 0, 0]
monkeys = [Monkey0(), Monkey1(), Monkey2(), Monkey3(), Monkey4(), Monkey5(), Monkey6(), Monkey7()]
for turn in range(rounds):
    for idx, monkey in enumerate(monkeys):
        for inspections in range(len(monkey.items)):
            monkey.inspect()
            monkey.bore()
            target, item_tossed = monkey.check()
            monkeys[target].catch(item_tossed)
            total_inspections[idx] += 1
total_inspections.sort()
print(f"Level of monkey business going on: {total_inspections[-1]*total_inspections[-2]}")

# %% Challenge 2: They're going bananas

# Luckily, we can run the same thing (but skip the "bore" part)
# Just need to reset each monkeys inventory
rounds = 10000
total_inspections = [0, 0, 0, 0, 0, 0, 0, 0]
monkeys = [Monkey0(), Monkey1(), Monkey2(), Monkey3(), Monkey4(), Monkey5(), Monkey6(), Monkey7()]
for turn in range(rounds):
    for idx, monkey in enumerate(monkeys):
        for inspections in range(len(monkey.items)):
            monkey.inspect()
            target, item_tossed = monkey.check()
            monkeys[target].catch(item_tossed)
            total_inspections[idx] += 1
total_inspections.sort()
print(f"Level of monkey business going on: {total_inspections[-1]*total_inspections[-2]}")
# TODO: Figure out a way to better store the worry levels, maybe using modulo
