# Modelo de datos MongoDB

```mermaid
erDiagram

    CUSTOMERS ||--o{ SALES : "customer_key"
    ITEMS ||--o{ SALES : "item_key"
    STORES ||--o{ SALES : "store_key"
    TIMES ||--o{ SALES : "time_key"
    PAYMENTS ||--o{ SALES : "payment_key"

    CUSTOMERS {
        string customer_key PK
        string name
    }

    ITEMS {
        string item_key PK
        string item_name
        string desc
        string unit
    }

    STORES {
        string store_key PK
        string division
        string district
        string upazila
    }

    TIMES {
        string time_key PK
        int year
        int month
        int day
    }

    PAYMENTS {
        string payment_key PK
        string trans_type
        string bank_name
    }

    SALES {
        string customer_key FK
        string item_key FK
        string store_key FK
        string time_key FK
        string payment_key FK
        number quantity
        number unit_price
        number total_price
    }