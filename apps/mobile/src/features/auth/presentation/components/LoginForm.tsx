import { View, TextInput, Text, Pressable } from 'react-native';
import { useLoginViewModel } from '../viewmodels/useLoginViewModel';
import { MaterialIcons } from '@expo/vector-icons';

export function LoginForm({ onSuccess }: { onSuccess: (u: any) => void }) {
    const vm = useLoginViewModel();
    const go = async () => {
        const r = await vm.submit();
        if (r.ok) onSuccess(r.user);
    };

    return (
        <View className="w-full flex-col">
            <View className={styles.inputContainer}>
                <MaterialIcons name="email" size={24} color="gray" />
                <TextInput
                    className={styles.input_text}
                    placeholderTextColor="#9CA3AF"
                    placeholder="Correo electrónico"
                    value={vm.email}
                    onChangeText={vm.setEmail}
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
                    value={vm.password}
                    autoCapitalize="none"
                    secureTextEntry
                    onChangeText={vm.setPassword}
                />
            </View>
            {vm.error && <Text>{vm.error}</Text>}
            <Pressable
                style={styles.shadow}
                className="mb-2 justify-center rounded-full bg-[#0071CE] p-4"
                onPress={go}
                disabled={vm.loading}
            >
                <Text className="text-center font-bold text-white">
                    {vm.loading ? 'Ingresando...' : 'Iniciar Sesión'}
                </Text>
            </Pressable>
        </View>
    );
}

const styles = {
    inputContainer: `flex-row items-center rounded-[2vw] bg-[#e7e6e6] py-3 px-4 mb-3`,
    input_text: `ml-2 flex-1 text-[#9F9F9F]`,
    button: `mb-2 justify-center rounded-full bg-[#0071CE] p-2`,
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
