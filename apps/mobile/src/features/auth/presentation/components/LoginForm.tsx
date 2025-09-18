import { View, TextInput, Text, Pressable } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { useState } from 'react';

export function LoginForm({
    onSubmit,
}: {
    onSubmit: (form: { email: string; password: string }) => void;
}) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = () => {
        setLoading(true);
        try {
            onSubmit({ email, password });
        } catch (err) {
            setError(
                err instanceof Error
                    ? err.message
                    : 'Error en el inicio de sesión'
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <View className="w-full">
            <View className={styles.inputContainer}>
                <MaterialIcons name="email" size={24} color="gray" />
                <TextInput
                    className={styles.input_text}
                    placeholderTextColor="#9CA3AF"
                    placeholder="Correo electrónico"
                    value={email}
                    onChangeText={setEmail}
                    autoCapitalize="none"
                    keyboardType="email-address"
                />
            </View>
            <View className={styles.inputContainer}>
                <MaterialIcons name="lock" size={24} color="gray" />
                <TextInput
                    placeholderTextColor="#9CA3AF"
                    className={styles.input_text}
                    placeholder="Contraseña"
                    value={password}
                    autoCapitalize="none"
                    secureTextEntry
                    onChangeText={setPassword}
                />
            </View>
            {error ? (
                <Text className="mb-2 text-center text-red-500">{error}</Text>
            ) : null}
            <Pressable
                style={styles.shadow}
                className="mb-2 justify-center rounded-full bg-[#0071CE] p-4"
                onPress={handleSubmit}
                disabled={loading}
            >
                <Text className="text-center font-bold text-white">
                    {loading ? 'Ingresando...' : 'Iniciar Sesión'}
                </Text>
            </Pressable>
        </View>
    );
}

const styles = {
    inputContainer: `flex-row items-center rounded-[2vw] bg-[#e7e6e6] py-3 px-4 mb-3`,
    input_text: `ml-2 text-[#9F9F9F]`,
    shadow: {
        // iOS
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.25,
        shadowRadius: 3.84,

        // Android
        elevation: 3,
    },
};
