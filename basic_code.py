class Orchard:
    def __init__(self, orchard_id):
        self.orchard_id = orchard_id
        self.zones = {}

    def add_zone(self, zone_id):
        self.zones[zone_id] = Zone(self.orchard_id, zone_id)

    def get_zone(self, zone_id):
        return self.zones.get(zone_id, None)

    def __repr__(self):
        return f"Orchard({self.orchard_id})"


class Zone:
    def __init__(self, orchard_id, zone_id):
        self.orchard_id = orchard_id
        self.zone_id = zone_id
        self.trees = {}

    def add_tree(self, tree_id):
        self.trees[tree_id] = Tree(self.orchard_id, self.zone_id, tree_id)

    def get_tree(self, tree_id):
        return self.trees.get(tree_id, None)

    def __repr__(self):
        return f"Zone({self.orchard_id}-{self.zone_id})"


class Tree:
    def __init__(self, orchard_id, zone_id, tree_id):
        self.orchard_id = orchard_id
        self.zone_id = zone_id
        self.tree_id = tree_id
        self.activities = []

    def add_activity(self, activity_id):
        activity_code = f"{self.orchard_id}-{self.zone_id}-{self.tree_id}-{activity_id}"
        self.activities.append(activity_code)

    def __repr__(self):
        return f"Tree({self.orchard_id}-{self.zone_id}-{self.tree_id})"


# 示例使用
# 创建一个果园
orchard = Orchard("O001")

# 添加分区
orchard.add_zone("Z01")
orchard.add_zone("Z02")

# 获取分区
zone_z01 = orchard.get_zone("Z01")

# 添加果树到分区Z01
zone_z01.add_tree("T001")
zone_z01.add_tree("T002")

# 获取果树
tree_t001 = zone_z01.get_tree("T001")

# 添加农事活动到果树T001
tree_t001.add_activity("A01")
tree_t001.add_activity("A02")

# 打印果园结构
print(orchard)
print(zone_z01)
print(tree_t001)
print(tree_t001.activities)
