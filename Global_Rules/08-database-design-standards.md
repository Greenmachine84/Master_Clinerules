# Database Design Standards

## Universal Database Principles

### Schema Design Standards
- **Normalization Guidelines**: Apply 3NF for most cases, denormalize for performance when needed
- **Naming Conventions**: Use consistent, descriptive names for tables, columns, and constraints
- **Data Types**: Choose appropriate data types for efficiency and accuracy
- **Indexing Strategy**: Index for query performance, avoid over-indexing
- **Referential Integrity**: Use foreign keys and constraints to maintain data consistency

### Table Naming Conventions
```sql
-- Use plural nouns for table names
users, orders, products, order_items

-- Use descriptive column names
created_at, updated_at, email_address, first_name

-- Use consistent prefixes for related tables
user_profiles, user_preferences, user_sessions
```

### Universal Column Standards
```sql
-- Standard audit columns for all tables
id              BIGINT PRIMARY KEY AUTO_INCREMENT,
created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
deleted_at      TIMESTAMP NULL,  -- For soft deletes

-- Standard user reference
created_by      BIGINT REFERENCES users(id),
updated_by      BIGINT REFERENCES users(id)
```

## Project-Specific Implementation Instructions

### For Each New Project
**Create in project root**: `database/`
```
database/
├── schema/
│   ├── tables/          # Table definitions
│   ├── indexes/         # Index definitions
│   ├── constraints/     # Constraint definitions
│   └── views/           # View definitions
├── migrations/          # Migration files
├── seeds/              # Test data
└── documentation/
    ├── ERD.md          # Entity Relationship Diagram
    ├── data-dictionary.md
    └── query-patterns.md
```

### Database-Specific Configurations
**Create in project `.clinerules/`**: `database-standards.md`
Include:
- Database engine choice (PostgreSQL, MySQL, SQLite)
- Connection pooling configuration
- Backup and recovery procedures
- Performance monitoring setup
- Environment-specific configurations

## Migration Standards

### Universal Migration Principles
- **Version Control**: Track all schema changes through migrations
- **Backward Compatibility**: Ensure migrations can be rolled back safely
- **Incremental Changes**: Make small, atomic changes per migration
- **Data Migration Safety**: Backup data before destructive operations
- **Testing**: Test migrations on copy of production data

### Migration File Structure
```python
# Example Flask-Migrate structure
"""Add user profiles table

Revision ID: 001_add_user_profiles
Revises: None
Create Date: 2024-01-15 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '001_add_user_profiles'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create table
    op.create_table('user_profiles',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('display_name', sa.String(100), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    
    # Create indexes
    op.create_index('idx_user_profiles_user_id', 'user_profiles', ['user_id'])

def downgrade():
    op.drop_index('idx_user_profiles_user_id', table_name='user_profiles')
    op.drop_table('user_profiles')
```

### Project-Specific Migration Instructions
**Create in project `database/documentation/`**: `migration-procedures.md`
Include:
- Migration tool setup and configuration
- Development vs production migration procedures
- Rollback procedures and safety checks
- Data migration patterns and best practices
- Migration testing procedures

## Indexing Strategy

### Universal Indexing Principles
- **Primary Keys**: Every table must have a primary key
- **Foreign Keys**: Index all foreign key columns
- **Query-Based Indexing**: Create indexes based on actual query patterns
- **Composite Indexes**: Use multi-column indexes for complex queries
- **Index Monitoring**: Regularly analyze index usage and performance

### Common Index Patterns
```sql
-- Single column indexes for frequently queried columns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_created_at ON orders(created_at);

-- Composite indexes for complex queries
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
CREATE INDEX idx_products_category_price ON products(category_id, price);

-- Partial indexes for filtered queries (PostgreSQL)
CREATE INDEX idx_active_users ON users(email) WHERE deleted_at IS NULL;

-- Functional indexes for computed values
CREATE INDEX idx_users_lower_email ON users(LOWER(email));
```

### Project-Specific Indexing Instructions
**Create in project `database/indexes/`**: `index-strategy.md`
Include:
- Application-specific query patterns
- Performance requirements and targets
- Index monitoring and maintenance procedures
- Database-specific indexing features and optimizations

## Query Optimization

### Universal Query Standards
- **Use Prepared Statements**: Prevent SQL injection and improve performance
- **Limit Result Sets**: Use LIMIT/OFFSET or cursor-based pagination
- **Avoid N+1 Queries**: Use joins or batch queries instead of loops
- **Select Specific Columns**: Avoid SELECT * in application queries
- **Use Query Analysis**: Analyze query execution plans regularly

### Efficient Query Patterns
```python
# Good: Batch loading with joins
def get_users_with_profiles(user_ids):
    return db.session.query(User, UserProfile)\
        .join(UserProfile, User.id == UserProfile.user_id)\
        .filter(User.id.in_(user_ids))\
        .all()

# Good: Pagination with cursor
def get_paginated_orders(cursor=None, limit=20):
    query = db.session.query(Order)\
        .order_by(Order.created_at.desc(), Order.id.desc())
    
    if cursor:
        query = query.filter(
            or_(
                Order.created_at < cursor['created_at'],
                and_(
                    Order.created_at == cursor['created_at'],
                    Order.id < cursor['id']
                )
            )
        )
    
    return query.limit(limit).all()

# Good: Aggregate in database
def get_user_order_stats(user_id):
    return db.session.query(
        func.count(Order.id).label('total_orders'),
        func.sum(Order.total_amount).label('total_spent'),
        func.max(Order.created_at).label('last_order_date')
    ).filter(Order.user_id == user_id).first()
```

### Project-Specific Query Instructions
**Create in project `database/documentation/`**: `query-patterns.md`
Include:
- Common application query patterns
- Performance requirements and benchmarks
- Query optimization procedures
- Monitoring and alerting for slow queries

## Data Integrity and Constraints

### Universal Constraint Standards
- **NOT NULL Constraints**: Use for required fields
- **CHECK Constraints**: Validate data ranges and formats
- **UNIQUE Constraints**: Ensure data uniqueness
- **Foreign Key Constraints**: Maintain referential integrity
- **Default Values**: Provide sensible defaults

```sql
-- Example table with comprehensive constraints
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT chk_email_format CHECK (email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT chk_password_length CHECK (LENGTH(password_hash) >= 8)
);
```

### Project-Specific Constraint Instructions
**Create in project `database/constraints/`**: `data-validation.md`
Include:
- Business rule constraints specific to the application
- Data validation requirements
- Custom constraint implementations
- Constraint monitoring and violation handling

## Database Security

### Universal Security Principles
- **Principle of Least Privilege**: Grant minimum necessary permissions
- **Database User Separation**: Use different users for different purposes
- **Connection Security**: Use SSL/TLS for database connections
- **Backup Security**: Encrypt backups and control access
- **Audit Trail**: Log database access and changes

### Database User Management
```sql
-- Application user with limited privileges
CREATE USER 'app_user'@'%' IDENTIFIED BY 'secure_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON app_database.* TO 'app_user'@'%';

-- Read-only user for analytics
CREATE USER 'analytics_user'@'%' IDENTIFIED BY 'secure_password';
GRANT SELECT ON app_database.* TO 'analytics_user'@'%';

-- Migration user with schema privileges
CREATE USER 'migration_user'@'%' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON app_database.* TO 'migration_user'@'%';
```

### Project-Specific Security Instructions
**Create in project `database/documentation/`**: `security-procedures.md`
Include:
- Database user management procedures
- Connection security configuration
- Backup and recovery security
- Compliance requirements and auditing
- Incident response procedures

## Performance Monitoring

### Universal Monitoring Standards
- **Query Performance**: Monitor slow queries and execution times
- **Connection Monitoring**: Track connection pool usage
- **Storage Monitoring**: Monitor disk usage and growth
- **Index Usage**: Track index efficiency and unused indexes
- **Lock Monitoring**: Monitor for deadlocks and long-running transactions

### Monitoring Implementation
```python
# Example SQLAlchemy event listeners for monitoring
from sqlalchemy import event
from sqlalchemy.engine import Engine
import time
import logging

logger = logging.getLogger('db_monitor')

@event.listens_for(Engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = time.time()

@event.listens_for(Engine, "after_cursor_execute")
def receive_after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - context._query_start_time
    
    if total > 0.1:  # Log queries taking more than 100ms
        logger.warning(f"Slow query ({total:.2f}s): {statement[:200]}...")
    
    # Store metrics for analysis
    store_query_metrics(statement, total, parameters)
```

### Project-Specific Monitoring Instructions
**Create in project `database/documentation/`**: `monitoring-setup.md`
Include:
- Monitoring tool configuration
- Performance alert thresholds
- Monitoring dashboard setup
- Performance baseline establishment
- Capacity planning procedures

## Backup and Recovery

### Universal Backup Principles
- **Regular Backups**: Automated daily backups minimum
- **Backup Testing**: Regularly test backup restoration
- **Multiple Backup Types**: Full, incremental, and transaction log backups
- **Offsite Storage**: Store backups in different geographic locations
- **Recovery Time Objectives**: Define RTO and RPO requirements

### Backup Strategy Template
```bash
#!/bin/bash
# Example backup script template

# Configuration
DB_NAME="app_database"
BACKUP_DIR="/backups/database"
RETENTION_DAYS=30
S3_BUCKET="company-db-backups"

# Create backup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.sql.gz"

mysqldump --single-transaction --routines --triggers \
    ${DB_NAME} | gzip > ${BACKUP_FILE}

# Upload to S3
aws s3 cp ${BACKUP_FILE} s3://${S3_BUCKET}/

# Cleanup old backups
find ${BACKUP_DIR} -name "${DB_NAME}_*.sql.gz" \
    -mtime +${RETENTION_DAYS} -delete
```

### Project-Specific Backup Instructions
**Create in project `database/documentation/`**: `backup-procedures.md`
Include:
- Backup schedule and retention policies
- Recovery procedures and testing
- Disaster recovery planning
- Backup monitoring and alerting
- Compliance requirements for backups

## Database Documentation

### Universal Documentation Standards
- **Entity Relationship Diagrams**: Visual representation of database structure
- **Data Dictionary**: Comprehensive column and table documentation
- **API Documentation**: Document database access patterns
- **Change Log**: Track schema changes and reasons
- **Performance Baselines**: Document expected performance characteristics

### Documentation Template Structure
**Create in project `database/documentation/`**:
```
documentation/
├── ERD.md                 # Entity relationship diagram
├── data-dictionary.md     # Table and column documentation
├── api-patterns.md        # Common query patterns
├── performance-baseline.md # Performance expectations
├── troubleshooting.md     # Common issues and solutions
└── changelog.md           # Schema change history
```

## Quality Checklist

Before deploying database changes, ensure:
- [ ] Schema changes are versioned through migrations
- [ ] Appropriate indexes are created for query patterns
- [ ] Data integrity constraints are implemented
- [ ] Security permissions are properly configured
- [ ] Backup and recovery procedures are tested
- [ ] Performance impact is analyzed and acceptable
- [ ] Documentation is updated
- [ ] Migration rollback procedures are verified
- [ ] Monitoring and alerting are configured
- [ ] Data migration scripts are tested with production-like data
