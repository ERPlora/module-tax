"""Pytest fixtures for tax module tests."""
import uuid
import pytest
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth.hashers import make_password

from apps.accounts.models import LocalUser
from apps.configuration.models import HubConfig, StoreConfig
from tax.models import TaxRate, TaxReport


@pytest.fixture
def hub_id():
    """Test hub_id."""
    return uuid.uuid4()


@pytest.fixture
def configured_hub(db, hub_id):
    """Configure HubConfig with test hub_id."""
    HubConfig._clear_cache()
    config = HubConfig.get_config()
    config.hub_id = hub_id
    config.is_configured = True
    config.save()
    return config


@pytest.fixture
def store_config(db):
    """StoreConfig for testing."""
    config = StoreConfig.get_solo()
    config.business_name = 'Test Store'
    config.tax_rate = Decimal('21.00')
    config.is_configured = True
    config.save()
    return config


@pytest.fixture
def admin_user(db, hub_id):
    """Admin user for testing."""
    return LocalUser.objects.create(
        hub_id=hub_id,
        name='Admin User',
        email='admin@test.com',
        role='admin',
        pin_hash=make_password('1234'),
        is_active=True,
    )


@pytest.fixture
def auth_client(client, admin_user, store_config):
    """Authenticated client with session."""
    session = client.session
    session['local_user_id'] = str(admin_user.id)
    session['user_name'] = admin_user.name
    session['user_email'] = admin_user.email
    session['user_role'] = admin_user.role
    session['hub_id'] = str(admin_user.hub_id)
    session['store_config_checked'] = True
    session.save()
    return client


@pytest.fixture
def tax_rate(db, hub_id):
    """Create a test TaxRate."""
    return TaxRate.objects.create(
        hub_id=hub_id,
        name='Test Name',
        rate=Decimal('10.00'),
        tax_type='Test Tax Type',
        is_default=False,
        is_active=True,
    )


@pytest.fixture
def tax_report(db, hub_id):
    """Create a test TaxReport."""
    return TaxReport.objects.create(
        hub_id=hub_id,
        name='Test Name',
        period_start=timezone.now().date(),
        period_end=timezone.now().date(),
        total_collected=Decimal('100.00'),
        total_paid=Decimal('100.00'),
        net_amount=Decimal('100.00'),
    )

