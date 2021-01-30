from rest_framework import serializers


class PassphraseSerializer(serializers.Serializer):
    passphrases = serializers.CharField()

    def create(self, validated_data):
        return {
            'passphrases': validated_data['passphrases'].split('\n'),
        }
