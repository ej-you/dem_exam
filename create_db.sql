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
