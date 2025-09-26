import {
    View,
    Text,
    Image,
    Pressable,
    ScrollView,
    KeyboardAvoidingView,
    Platform,
    TouchableOpacity,
    Alert,
} from 'react-native';
import { useState } from 'react';
import { LoginForm } from '../components/LoginForm';
import { useAuth } from '~/src/features/auth/presentation/providers/AuthProvider';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';

export const LoginScreen = () => {
    const { login, isLoading } = useAuth();
    const [error, setError] = useState<string | null>(null);

    const router = useRouter();

    const handleLogin = async (form: { email: string; password: string }) => {
        try {
            setError(null);
            await login(form.email, form.password);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to login');
            Alert.alert(
                'Login Failed',
                err instanceof Error ? err.message : 'Something went wrong'
            );
        }
    };

    return (
        <SafeAreaView className="flex-1 bg-white">
            <KeyboardAvoidingView
                behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
                style={{ flex: 1 }}
            >
                <ScrollView
                    contentContainerStyle={{ flexGrow: 1 }}
                    keyboardShouldPersistTaps="handled"
                >
                    <View className="flex-1 items-center justify-center px-10">
                        <View className="w-full max-w-sm">
                            <View className="mb-6 items-center">
                                <Text
                                    style={style.shadow_text}
                                    className="text-5xl font-bold text-[#0062BF]"
                                >
                                    TemuComercio
                                </Text>

                                <View className="my-4 max-h-[200px] min-h-[80px] justify-center">
                                    <Image
                                        className="aspect-square w-3/5 min-w-[80px] max-w-[200px]"
                                        source={require('~/assets/adaptive-icon-recortado.png')}
                                        resizeMode="contain"
                                    />
                                </View>
                            </View>

                            <View className="px-4">
                                <LoginForm onSubmit={handleLogin} />
                                <TouchableOpacity
                                    className="p-2"
                                    onPress={() =>
                                        router.push('/(auth)/recoveryPassword')
                                    }
                                >
                                    <Text className="text-center text-gray-500 underline ">
                                        ¿Olvidaste tu contraseña? Apresiona aquí
                                    </Text>
                                </TouchableOpacity>
                            </View>
                        </View>
                    </View>
                </ScrollView>
            </KeyboardAvoidingView>
        </SafeAreaView>
    );
};

const style = {
    shadow: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.25,
        shadowRadius: 3.84,
        elevation: 2,
    },
    shadow_text: {
        textShadowColor: 'rgba(0,0,0,0.3)',
        textShadowOffset: { width: 0, height: 3 },
        textShadowRadius: 4,
    },
};
