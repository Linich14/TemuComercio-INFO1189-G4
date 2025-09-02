import { View, Text, Image, Pressable } from 'react-native';
import {
    KeyboardAwareScrollView,
    KeyboardToolbar,
} from 'react-native-keyboard-controller';
import { LoginForm } from '../components/LoginForm';
import { useAuth } from '~/src/providers/AuthProvider';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';

export const LoginScreen = () => {
    const { signIn } = useAuth();
    const router = useRouter();

    return (
        <>
            <KeyboardAwareScrollView
                // Ajusta si personalizas la altura de la toolbar
                bottomOffset={62}
                keyboardShouldPersistTaps="handled"
                contentContainerStyle={{ flexGrow: 1 }}
            >
                <SafeAreaView className="flex-1">
                    <View className="flex-1 items-center justify-center px-10">
                        <Text
                            style={style.shadow_text}
                            className="text-5xl font-bold text-[#0062BF]"
                        >
                            TemuComercio
                        </Text>

                        <View className="my-4 max-h-[200px] min-h-[80px] items-center justify-center">
                            <Image
                                className="aspect-square w-3/5 min-w-[80px] max-w-[200px]"
                                source={require('~/assets/adaptive-icon-recortado.png')}
                                resizeMode="contain"
                            />
                        </View>

                        <View className="w-full">
                            {/* Asegúrate de que los TextInput del LoginForm estén dentro de este árbol */}
                            <LoginForm onSuccess={signIn} />

                            <View className="mt-2 w-full">
                                <Pressable
                                    style={style.shadow}
                                    className="group rounded-full bg-white p-4 active:bg-[#0071CE]"
                                    onPress={() =>
                                        router.push('/(auth)/Register')
                                    }
                                >
                                    <Text className="text-center font-bold text-[#0071CE] group-active:text-white">
                                        Registrarse
                                    </Text>
                                </Pressable>
                            </View>
                        </View>
                    </View>
                </SafeAreaView>
            </KeyboardAwareScrollView>

            {/* Barra nativa con “cerrar teclado” y navegación entre campos */}
            <KeyboardToolbar />
        </>
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
