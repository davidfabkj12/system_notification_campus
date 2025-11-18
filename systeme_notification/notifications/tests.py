from django.test import SimpleTestCase, TestCase
from datetime import datetime, timedelta
from django.utils import timezone
from unittest.mock import patch

from .core import Epidemie, Incendie, Innondation, Securite
from .decorators import (
    AddPerformanceTracking,
    AutoConfigurationValidation,
    RegisterInGlobalRegistry,
    AddCircuitBreaker,
    message,
    global_registry,
)
from .descriptors import EmailDescriptor, PhoneDescriptor, PriorityDescriptor, TimeWindowDescriptor
from .metaclasses import NotificationMeta, NotificationRegistry, ChannelMeta, TemplateMeta, ConfigMeta

# -------------------------------
# Tests des classes d'urgences
# -------------------------------
class UrgenceTests(TestCase):
    def test_epidemie_evacuer(self):
        # Vérifie que la méthode evacuer() fonctionne pour Epidemie
        e = Epidemie()
        e.evacuer()

    def test_incendie_evacuer(self):
        # Vérifie que la méthode evacuer() fonctionne pour Incendie
        i = Incendie()
        i.evacuer()

    def test_innondation_evacuer(self):
        # Vérifie que la méthode evacuer() fonctionne pour Innondation
        n = Innondation()
        n.evacuer()

    def test_securite_evacuer(self):
        # Vérifie que la méthode evacuer() fonctionne pour Securite
        s = Securite()
        s.evacuer()


# -------------------------------
# Tests des décorateurs
# -------------------------------
class DecoratorTests(SimpleTestCase):
    def test_message_decorator_logs_call_and_return(self):
        # Vérifie que le décorateur @message affiche un log avant et après l'appel
        class Foo:
            @message
            def bar(self):
                return "baz"

        with patch('builtins.print') as mock_print:
            result = Foo().bar()
            self.assertEqual(result, "baz")
            # Vérifie que "Appel de bar" est loggé
            self.assertTrue(
                any("Appel de bar" in call.args[0] for call in mock_print.call_args_list)
            )
            # Vérifie que "Fin de bar" est loggé
            self.assertTrue(
                any("Fin de bar" in call.args[0] for call in mock_print.call_args_list)
            )

    def test_add_performance_tracking_injects_time_window(self):
        # Vérifie que le décorateur ajoute un attribut time_window
        @AddPerformanceTracking()
        class Dummy:
            def __init__(self):
                pass
            def evacuer(self):
                return "done"

        d = Dummy()
        with patch('builtins.print'):
            result = d.evacuer()
        self.assertEqual(result, "done")
        self.assertTrue(hasattr(d, 'time_window'))
        tw = d.time_window
        # Vérifie que time_window est un tuple (start, end)
        self.assertIsInstance(tw, tuple)
        self.assertEqual(len(tw), 2)
        self.assertLess(tw[0], tw[1])

    def test_auto_configuration_validation_raises_for_missing_fields(self):
        # Vérifie que le décorateur impose la présence des champs requis
        @AutoConfigurationValidation()
        class Dummy:
            required_fields = ['foo', 'bar']
            def __init__(self, foo=None, bar=None):
                if foo is not None:
                    self.foo = foo
                if bar is not None:
                    self.bar = bar

        # Doit lever une erreur si les champs requis sont absents
        with self.assertRaises(ValueError):
            Dummy()
        with self.assertRaises(ValueError):
            Dummy(foo=1)
        # Cas valide
        d = Dummy(foo=1, bar=2)
        self.assertEqual(getattr(d, 'foo'), 1)

    def test_register_in_global_registry_adds_class(self):
        # Vérifie que la classe est bien enregistrée dans le registre global
        global_registry.clear()
        @RegisterInGlobalRegistry()
        class Dummy:
            pass
        self.assertIn('Dummy', global_registry)
        self.assertIs(global_registry['Dummy'], Dummy)

    def test_add_circuit_breaker_catches_exceptions(self):
        # Vérifie que le décorateur intercepte les exceptions et retourne None
        @AddCircuitBreaker()
        class Dummy:
            def evacuer(self):
                raise RuntimeError("boom")

        d = Dummy()
        with patch('builtins.print'):
            result = d.evacuer()
        self.assertIsNone(result)


# -------------------------------
# Tests des descripteurs
# -------------------------------
class DescriptorTests(SimpleTestCase):
    """Tests des descripteurs personnalisés : email, téléphone, priorité et fenêtre temporelle."""

    def test_email_descriptor_validates_format(self):
        # Vérifie que le descripteur email valide le format
        class Dummy:
            email = EmailDescriptor()
        d = Dummy()
        d.email = 'test@example.com'
        self.assertEqual(d.email, 'test@example.com')
        with self.assertRaises(ValueError):
            d.email = 'not-an-email'

    def test_phone_descriptor_validates_format(self):
        # Vérifie que le descripteur téléphone valide le format international
        class Dummy:
            phone = PhoneDescriptor()
        d = Dummy()
        d.phone = '+12345678901'
        self.assertEqual(d.phone, '+12345678901')
        with self.assertRaises(ValueError):
            d.phone = '012345'

    def test_priority_descriptor_normalizes_and_validates(self):
        # Vérifie que le descripteur priorité normalise et valide les valeurs
        class Dummy:
            priority = PriorityDescriptor()
        d = Dummy()
        self.assertEqual(d.priority, 'faible')  # valeur par défaut
        d.priority = 'haute'
        self.assertEqual(d.priority, 'haute')
        d.priority = 'Moyenne'
        self.assertEqual(d.priority, 'moyenne')
        d.priority = 'URgente'
        self.assertEqual(d.priority, 'urgente')
        with self.assertRaises(ValueError):
            d.priority = 'unknown'

    def test_time_window_descriptor_validates_tuple(self):
        # Vérifie que le descripteur time_window accepte un tuple (start, end)
        class Dummy:
            time_window = TimeWindowDescriptor()
        d = Dummy()
        start = datetime(2020, 1, 1)
        end = datetime(2020, 1, 2)
        d.time_window = (start, end)
        self.assertEqual(d.time_window, (start, end))
        with self.assertRaises(ValueError):
            d.time_window = 'invalid'
        with self.assertRaises(ValueError):
            d.time_window = (start,)


# -------------------------------
# Tests des métaclasses
# -------------------------------
class MetaclassTests(SimpleTestCase):
    """Tests des métaclasses définies dans metaclasses.py."""

    def test_notification_meta_adds_fields_and_registers(self):
        # Vérifie que NotificationMeta ajoute des champs et enregistre la classe
        class TestNotif(metaclass=NotificationMeta):
            required_fields = ['name']
            def __init__(self, name=None):
                self.name = name

        self.assertTrue(hasattr(TestNotif, 'validate_required_fields'))
        self.assertEqual(TestNotif.description, 'Notificateur de type TestNotif')
        self.assertEqual(TestNotif._notification_type, 'testnotif')
        self.assertIs(NotificationRegistry.get('TestNotif'), TestNotif)

        with self.assertRaises(ValueError):
            tn = TestNotif()
            tn.validate_required_fields()

        tn = TestNotif(name='OK')
        tn.validate_required_fields()

    def test_channel_meta_sets_channel_name(self):
        # Vérifie que ChannelMeta définit correctement le nom du canal
        class SmsChannel(metaclass=ChannelMeta):
            pass
        self.assertEqual(SmsChannel.channel_name, 'smschannel')

    def test_template_meta_adds_render_template(self):
        # Vérifie que TemplateMeta ajoute une méthode render_template
        class MyTemplate(metaclass=TemplateMeta):
            template_fields = {'field1': 'value1'}
        mt = MyTemplate()
        self.assertTrue(hasattr(mt, 'render_template'))
        self.assertIn('field1', mt.render_template())

    def test_config_meta_validates_config_type(self):
        # Vérifie que ConfigMeta impose un dictionnaire comme config
        class GoodConfig(metaclass=ConfigMeta):
            config = {'key': 'value'}
        self.assertTrue(hasattr(GoodConfig, 'config'))

        with self.assertRaises(ValueError):
            class BadConfig(metaclass=ConfigMeta):
                config = 'not-a-dict'
