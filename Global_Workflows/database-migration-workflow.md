# Database Migration Workflow

## Purpose
Safe and reliable database schema changes and data migrations for the ADA application.

## Prerequisites
- Database backup created
- Migration scripts tested in development
- Rollback plan documented
- Maintenance window scheduled

## Steps

### 1. Pre-Migration Setup
```bash
# Create full database backup
pg_dump -h localhost -U postgres ada_database > backup_pre_migration.sql

# Verify backup integrity
pg_restore --list backup_pre_migration.sql

# Document current schema version
flask db current > schema_version_pre.txt
```

### 2. Migration Script Review
- Review all SQL changes
- Validate migration logic
- Check for potential data loss
- Verify rollback procedures

### 3. Development Testing
```bash
# Test migration in development
flask db upgrade

# Verify data integrity
python -c "
import app
from app import db
# Add validation queries here
"

# Test rollback
flask db downgrade
```

### 4. Staging Environment Test
- Apply migration to staging
- Run full application test suite
- Validate data consistency
- Test rollback procedure

### 5. Production Migration
```bash
# Put application in maintenance mode
sudo systemctl stop ada-app

# Apply migration
flask db upgrade

# Verify migration success
flask db current
```

### 6. Post-Migration Validation
```python
# Data integrity checks
def validate_migration():
    # Check record counts
    assert User.query.count() > 0
    
    # Validate relationships
    for user in User.query.all():
        assert user.profile is not None
    
    # Check data types
    # Add specific validation logic
    
    print("Migration validation successful")
```

### 7. Application Restart
```bash
# Start application
sudo systemctl start ada-app

# Monitor application logs
tail -f /var/log/ada-app/application.log

# Test critical functions
curl -f https://your-domain.com/api/health
```

## Migration Types

### Schema Changes
- Adding/removing columns
- Changing data types
- Adding/removing indexes
- Constraint modifications

### Data Migrations
- Data transformations
- Table restructuring
- Reference updates
- Cleanup operations

## Safety Measures
- Always backup before migration
- Test in non-production first
- Have rollback plan ready
- Monitor during migration
- Validate after completion

## Rollback Procedure
```bash
# If migration fails:
sudo systemctl stop ada-app

# Restore database backup
dropdb ada_database
createdb ada_database
pg_restore -d ada_database backup_pre_migration.sql

# Revert application code if needed
git checkout previous-version

# Restart application
sudo systemctl start ada-app
```

## Best Practices
- Small, incremental changes
- Backward compatible when possible
- Comprehensive testing
- Clear rollback strategy
- Monitor performance impact
- Document all changes
