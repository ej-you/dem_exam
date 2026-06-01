-- **** --
-- User --
-- **** --

-- Таблица ролей
CREATE TABLE roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Таблица пользователей
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    role_id INT NOT NULL,
    fullname VARCHAR(150) NOT NULL,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Индексы
CREATE INDEX idx_users_role_id ON users(role_id);
CREATE INDEX idx_users_username ON users(username);
CREATE UNIQUE INDEX idx_users_username_unique ON users(username);

-- Вставка ролей
INSERT INTO roles (name) VALUES
    ('admin'),
    ('client'),
    ('manager');

-- Вставка пользователей
INSERT INTO users (role_id, fullname, username, password) VALUES
    (1, 'Администратор Системы', 'admin', 'admin123'),
    (2, 'Иван Иванов', 'client', 'client123'),
    (3, 'Мария Петрова', 'manager', 'manager123');


-- **** --
-- Good --
-- **** --


-- 1. Единицы измерения
CREATE TABLE measurement_units (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(25) NOT NULL
);

-- 2. Поставщики
CREATE TABLE suppliers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(50) NOT NULL
);

-- 3. Производители
CREATE TABLE producers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(50) NOT NULL
);

-- 4. Категории товаров
CREATE TABLE good_categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(35) NOT NULL
);

-- 5. Товары (главная таблица)
CREATE TABLE goods (
    id INT PRIMARY KEY AUTO_INCREMENT,
    article VARCHAR(10) NOT NULL,
    title VARCHAR(50) NOT NULL,
    measurement_unit_id INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    supplier_id INT NOT NULL,
    producer_id INT NOT NULL,
    good_category_id INT NOT NULL,
    discount INT NOT NULL DEFAULT 0,
    amount INT NOT NULL DEFAULT 0,
    description TEXT,
    photo VARCHAR(255) NOT NULL DEFAULT 'default_good.png',

    FOREIGN KEY (measurement_unit_id) REFERENCES measurement_units(id) ON DELETE RESTRICT,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE RESTRICT,
    FOREIGN KEY (producer_id) REFERENCES producers(id) ON DELETE RESTRICT,
    FOREIGN KEY (good_category_id) REFERENCES good_categories(id) ON DELETE RESTRICT
);

-- Индексы для оптимизации
CREATE INDEX idx_goods_article ON goods(article);
CREATE INDEX idx_goods_title ON goods(title);
CREATE INDEX idx_goods_price ON goods(price);
CREATE INDEX idx_goods_discount ON goods(discount);
CREATE INDEX idx_goods_amount ON goods(amount);

-- Составные индексы
CREATE INDEX idx_goods_category_price ON goods(good_category_id, price);
CREATE INDEX idx_goods_supplier_price ON goods(supplier_id, price);

INSERT INTO measurement_units (name) VALUES ('шт');

-- Поставщики
INSERT INTO suppliers (title) VALUES
    ('ООО "ТехноСнаб"'),
    ('ИП Иванов'),
    ('ООО "ТоргМастер"'),
    ('ЗАО "ОптТрейд"'),
    ('ООО "МегаСтрой"');

-- Производители
INSERT INTO producers (title) VALUES
    ('ООО "Сделано в России"'),
    ('Китайская корпорация "HuaWei"'),
    ('ООО "Электроника"'),
    ('ИП Петров'),
    ('ООО "СтройИндустрия"');

-- Категории товаров
INSERT INTO good_categories (name) VALUES
    ('Электроника'),
    ('Бытовая техника'),
    ('Стройматериалы'),
    ('Продукты питания'),
    ('Одежда'),
    ('Канцелярия');

-- Товары
INSERT INTO goods (article, title, measurement_unit_id, price, supplier_id, producer_id, good_category_id, discount, amount, description) VALUES
    ('A001', 'Смартфон X10', 1, 29999.99, 1, 2, 1, 10, 50, 'Современный смартфон с 128GB памяти'),
    ('A002', 'Ноутбук Pro', 1, 89999.99, 1, 1, 1, 5, 25, 'Мощный ноутбук для работы и игр'),
    ('B001', 'Микроволновая печь', 1, 5999.99, 2, 3, 2, 15, 100, 'Микроволновка с грилем'),
    ('B002', 'Холодильник', 1, 44999.99, 2, 3, 2, 0, 30, 'Двухкамерный холодильник'),
    ('C001', 'Цемент М500', 1, 350.00, 3, 4, 3, 0, 1000, 'Цемент в мешках по 50кг'),
    ('C002', 'Кирпич красный', 1, 15.50, 3, 4, 3, 0, 5000, 'Керамический кирпич'),
    ('D001', 'Яблоки', 1, 120.00, 4, 5, 4, 0, 200, 'Свежие яблоки'),
    ('D002', 'Молоко', 1, 89.99, 4, 5, 4, 5, 150, 'Пастеризованное молоко 3.2%'),
    ('E001', 'Футболка хлопок', 1, 999.99, 5, 1, 5, 20, 300, 'Хлопковая футболка'),
    ('F001', 'Ручка шариковая', 1, 15.00, 5, 2, 6, 0, 1000, 'Синяя ручка');
