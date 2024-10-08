# Generated by Django 5.1 on 2024-08-31 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barbeiro', '0006_remove_dadosbarbeiro_servicos'),
        ('clientes', '0002_agendamentos_servico_alter_agendamentos_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendamentos',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.RemoveField(
            model_name='agendamentos',
            name='servico',
        ),
        migrations.AddField(
            model_name='agendamentos',
            name='servico',
            field=models.ManyToManyField(to='barbeiro.servicos'),
        ),
    ]
