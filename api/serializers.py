from rest_framework import serializers
from .models import Contact, Label, LabelMap


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name']


class LabelMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabelMap
        fields = ['id', 'contact_id', 'label_id']


class ContactListSerializer(serializers.ModelSerializer):
    labels = LabelSerializer(many=True, read_only=True)

    class Meta:
        model = Contact
        fields = [
            'id', 'name', 'profile_image_url', 'email', 'phone',
            'company', 'job_title', 'memo', 'address', 'birthday', 'website', 'labels'
        ]