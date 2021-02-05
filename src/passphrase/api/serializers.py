from rest_framework import serializers


class PassphraseSerializer(serializers.Serializer):
    passphrases = serializers.CharField(style={'base_template': 'textarea.html'})

    def create(self, validated_data):
        return {
            'passphrases': map(lambda p: p.strip(), validated_data['passphrases'].split('\n')),
        }
