from rest_framework import serializers
from .models import Contact, Label, LabelMap


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name']


class LabelMapSerializer(serializers.ModelSerializer):
    contact = serializers.PrimaryKeyRelatedField(read_only=True)
    label = LabelSerializer(read_only=True)

    class Meta:
        model = LabelMap
        fields = ['id', 'contact_id', 'label_id', 'contact', 'label']


class ContactListSerializer(serializers.ModelSerializer):
    labels = LabelSerializer(many=True, read_only=True)

    class Meta:
        model = Contact
        fields = [
            'id', 'name', 'profile_image_url', 'email', 'phone',
            'company', 'job_title', 'labels'
        ]


class ContactDetailSerializer(serializers.ModelSerializer):
    labels = LabelSerializer(many=True, read_only=True)
    # label_ids = serializers.PrimaryKeyRelatedField(
    #     queryset=Label.objects.all(), many=True, write_only=True, required=False
    # )

    label_names = serializers.ListField(
        child=serializers.CharField(max_length=200),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Contact
        fields = [
            'id', 'name', 'profile_image_url', 'email', 'phone',
            'company', 'job_title', 'memo', 'address', 'birthday', 'website',
            'labels', 'label_names'
        ]
        read_only_fields = ['id', 'labels']

    def create(self, validated_data):
        label_names_data = validated_data.pop('label_names', [])

        contact = Contact.objects.create(**validated_data)

        for label_name in label_names_data:
            label, created = Label.objects.get_or_create(name=label_name)
            contact.labels.add(label)

        return contact

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance