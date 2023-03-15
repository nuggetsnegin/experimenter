# Generated by Django 3.2.5 on 2021-11-08 19:45

from django.db import migrations, models


def restore_feature_enabled(apps, schema_editor):
    NimbusExperiment = apps.get_model("experiments", "NimbusExperiment")
    for experiment in NimbusExperiment.objects.exclude(published_dto=None):
        for branch_data in experiment.published_dto.get("branches", []):
            branch_slug = branch_data.get("slug")
            if branch_slug and experiment.branches.filter(slug=branch_slug).exists():
                branch = experiment.branches.get(slug=branch_slug)
                branch.feature_enabled = branch_data.get("feature", {}).get(
                    "enabled", True
                )
                branch.save()


class Migration(migrations.Migration):

    dependencies = [
        ("experiments", "0195_nimbusexperiment_is_rollout"),
    ]

    operations = [
        migrations.AddField(
            model_name="nimbusbranch",
            name="feature_enabled",
            field=models.BooleanField(default=True),
        ),
        migrations.RunPython(restore_feature_enabled),
    ]