# Cấu trúc kế thừa:
# + ABC: Champion
# + Lớp con: Warrior, Mage
# Lớp cha Champion chỉ định nghĩa tính trừu tượng, bắt buộc các lớp con phải ghi đè để tự tính toán
# Khi studio muốn thêm hệ tướng mới, chỉ cần tạo lớp mới kế thừa từ Champion và thực hiện hàm calculate_skill_damage()

from abc import ABC, abstractmethod


class Champion(ABC):
    def __init__(self, champion_id, name, base_hp, base_atk):
        self.champion_id = champion_id
        self.name = name
        self.base_hp = base_hp if base_hp > 0 else 100
        self.base_atk = base_atk if base_atk > 0 else 100

    @abstractmethod
    def calculate_skill_damage(self):
        pass

    def get_combat_power(self):
        return self.base_hp + (self.calculate_skill_damage() * 1.5)

    def __add__(self, other):
        if isinstance(other, Champion):
            return self.get_combat_power() + other.get_combat_power()
        return self.get_combat_power() + other

    def __radd__(self, other):
        return self.__add__(other)

    def __gt__(self, other):
        if isinstance(other, Champion):
            return self.get_combat_power() > other.get_combat_power()
        return False


class Warrior(Champion):
    def __init__(self, champion_id, name, base_hp, base_atk, shield_bonus):
        super().__init__(champion_id, name, base_hp, base_atk)
        self.shield_bonus = shield_bonus

    def calculate_skill_damage(self):
        return self.base_atk * 2 + self.shield_bonus


class Mage(Champion):
    def __init__(self, champion_id, name, base_hp, base_atk, ability_power):
        super().__init__(champion_id, name, base_hp, base_atk)
        self.ability_power = ability_power

    def calculate_skill_damage(self):
        return self.base_atk * self.ability_power


def display_pool(pool):
    print("\n--- DANH SÁCH QUÂN CỜ TRONG BỂ TƯỚNG ---")
    print(f"{'Mã':<8} | {'Tên tướng':<18} | {'Hệ':<8} | {'HP':<6} | {'ATK':<5} | {'Chỉ số riêng':<15} | {'Chiến lực'}")
    print("-" * 90)
    for c in pool.values():
        class_name = c.__class__.__name__
        spec_info = f"Armor: {c.shield_bonus}" if class_name == "Warrior" else f"AP: {c.ability_power}"
        print(f"{c.champion_id:<8} | {c.name:<18} | {class_name:<8} | {c.base_hp:<6} | {c.base_atk:<5} | {spec_info:<15} | {c.get_combat_power():.0f}")
    print("-" * 90)


def add_champion(pool):
    print("\n--- TẠO TƯỚNG MỚI ---")
    print("1: Warrior")
    print("2: Mage")
    sub_choice = input("Chọn hệ tướng: ").strip()

    c_id = input("Nhập mã tướng: ").strip().upper()

    if c_id in pool:
        print(f"Lỗi: Mã tướng {c_id} đã tồn tại trong bể tướng!")
        return

    name = input("Nhập tên tướng: ").strip()
    hp = int(input("Nhập HP: "))
    atk = int(input("Nhập ATK: "))

    if sub_choice == "1":
        armor = int(input("Nhập Armor: "))
        new_champ = Warrior(c_id, name, hp, atk, armor)
        pool[c_id] = new_champ
        print(f"Thêm tướng Warrior thành công!")
        print(
            f"Mã: {c_id} | Tên: {name} | Chiến lực: {new_champ.get_combat_power():.0f}")
    elif sub_choice == "2":
        ap = float(input("Nhập Hệ số phép thuật (AP): "))
        new_champ = Mage(c_id, name, hp, atk, ap)
        pool[c_id] = new_champ
        print(f"Thêm tướng Mage thành công!")
        print(
            f"Mã: {c_id} | Tên: {name} | Chiến lực: {new_champ.get_combat_power():.0f}")
    else:
        print("Hệ tướng không hợp lệ!")


def compare_power(pool):
    print("\n--- SO SÁNH SỨC MẠNH 2 QUÂN CỜ ---")
    id1 = input("Nhập mã tướng thứ nhất: ").strip().upper()
    id2 = input("Nhập mã tướng thứ hai: ").strip().upper()

    if id1 not in pool or id2 not in pool:
        if id1 not in pool:
            print(f"Mã tướng {id1} không hợp lệ, bỏ qua!")
        if id2 not in pool:
            print(f"Mã tướng {id2} không hợp lệ, bỏ qua!")
        return

    c1 = pool[id1]
    c2 = pool[id2]
    print("\nThông tin so sánh:")
    print(f"{c1.champion_id} - {c1.name} | Hệ: {c1.__class__.__name__} | Chiến lực: {c1.get_combat_power():.0f}")
    print(f"{c2.champion_id} - {c2.name} | Hệ: {c2.__class__.__name__} | Chiến lực: {c2.get_combat_power():.0f}")

    if c1 > c2:
        print(
            f"Kết quả: {c1.champion_id} - {c1.name} mạnh hơn {c2.champion_id} - {c2.name}.")
    elif c2 > c1:
        print(
            f"Kết quả: {c2.champion_id} - {c2.name} mạnh hơn {c1.champion_id} - {c1.name}.")
    else:
        print(f"Kết quả: Hai quân cờ có sức mạnh ngang nhau.")


def calculate_total_power(pool):
    print("\n--- TÍNH TỔNG CHIẾN LỰC ĐỘI HÌNH RA SÂN ---")
    raw_input = input("Nhập danh sách mã tướng, cách nhau bằng dấu phẩy: ")
    input_ids = [i.strip().upper() for i in raw_input.split(",") if i.strip()]

    lineup = []
    for c_id in input_ids:
        if c_id in pool:
            lineup.append(pool[c_id])
        else:
            print(f"Mã tướng {c_id} không hợp lệ, bỏ qua!")

    if not lineup:
        print("Đội hình hiện đang rỗng.")
        return

    print("Danh sách đội hình:")
    for idx, champ in enumerate(lineup, 1):
        print(
            f"{idx}. {champ.champion_id} - {champ.name} | Chiến lực: {champ.get_combat_power():.0f}")

    total_power = sum(lineup)
    print(f"Tổng chiến lực đội hình: {total_power:.0f}")


def main():
    champion_pool = {
        "WAR01": Warrior("WAR01", "Rikkei Knight", 1200, 300, 150),
        "WAR02": Warrior("WAR02", "Steel Guardian", 1500, 250, 200),
        "MAG01": Mage("MAG01", "Rikkei Wizard", 800, 500, 1.5)
    }

    while True:
        print("\n=== RIKKEI RPG - AUTO-BATTLER MANAGER ===")
        print("1. Hiển thị bể tướng hiện có")
        print("2. Thêm quân cờ mới")
        print("3. So sánh 2 quân cờ")
        print("4. Tính tổng chiến lực đội hình ra sân")
        print("5. Thoát chương trình")
        choice = input("Chọn chức năng (1-5): ").strip()

        if choice == "1":
            display_pool(champion_pool)
        elif choice == "2":
            add_champion(champion_pool)
        elif choice == "3":
            compare_power(champion_pool)
        elif choice == "4":
            calculate_total_power(champion_pool)
        elif choice == "5":
            print("Cảm ơn bạn đã sử dụng Rikkei RPG - Auto-Battler Manager!")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng nhập từ 1 đến 5!")


if __name__ == "__main__":
    main()
