// app/(auth)/recoveryPassword.tsx
import React, { useMemo, useState } from 'react';
import { View, Text, Image, TextInput, Pressable, ActivityIndicator, Alert } from 'react-native';
import {
  KeyboardAwareScrollView,
  KeyboardToolbar,
} from 'react-native-keyboard-controller';
import { SafeAreaView } from 'react-native-safe-area-context';
import { MaterialIcons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
// Si tu AuthProvider expone algún método para reset, puedes importarlo aquí.
// import { useAuth } from '~/src/features/auth/presentation/providers/AuthProvider';

type ResetResult =
  | { ok: true }
  | { ok: false; message: string };

async function doSendReset(email: string): Promise<ResetResult> {
  // TODO: Reemplaza este stub por tu implementación real (Supabase/Firebase/API propia).
  // Ejemplo (Supabase):
  // const { error } = await supabase.auth.resetPasswordForEmail(email, {
  //   redirectTo: 'tuapp://reset', // si corresponde
  // });
  // if (error) return { ok: false, message: error.message };
  // return { ok: true };

  // Simulación de red:
  await new Promise((r) => setTimeout(r, 900));
  // Valida un caso de error simulado:
  if (email.toLowerCase().endsWith('@example.com')) {
    return { ok: false, message: 'Dominio no permitido. Intenta con otro correo.' };
  }
  return { ok: true };
}

export default function RecoveryPasswordScreen() {
  const router = useRouter();
  // const { requestPasswordReset } = useAuth(); // si lo tienes en tu provider

  const [email, setEmail] = useState('');
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sent, setSent] = useState(false);

  const disabled = useMemo(() => {
    if (sending) return true;
    const re = /\S+@\S+\.\S+/;
    if (!re.test(email)) return true;
    return false;
  }, [email, sending]);

  const onSubmit = async () => {
    setError(null);
    setSent(false);
    setSending(true);
    try {
      // Si lo manejas por tu AuthProvider, reemplaza por:
      // const res = await requestPasswordReset(email);
      const res = await doSendReset(email);
      if (res.ok) {
        setSent(true);
        Alert.alert(
          'Correo enviado',
          'Revisa tu bandeja de entrada y sigue las instrucciones para restablecer tu contraseña.'
        );
      } else {
        setError(res.message || 'No se pudo enviar el correo de recuperación.');
      }
    } catch (e: any) {
      setError(e?.message ?? 'Ha ocurrido un error inesperado.');
    } finally {
      setSending(false);
    }
  };

  return (
    <>
      <KeyboardAwareScrollView
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
              <Text className="mb-3 text-center text-xl font-semibold text-[#0062BF]">
                Recuperar contraseña
              </Text>

              {/* Campo de correo */}
              <View className="flex-row items-center gap-3 bg-white rounded-2xl px-4 py-3 border border-gray-200">
                <MaterialIcons name="email" size={22} color="gray" />
                <TextInput
                  className="flex-1 text-base text-gray-800"
                  placeholder="Correo electrónico"
                  placeholderTextColor="#9CA3AF"
                  value={email}
                  onChangeText={setEmail}
                  autoCapitalize="none"
                  keyboardType="email-address"
                  returnKeyType="done"
                  onSubmitEditing={() => {
                    if (!disabled) onSubmit();
                  }}
                />
              </View>

              {/* Info/estado */}
              {sent && (
                <Text className="mt-2 text-sm text-green-600 text-center">
                  ¡Listo! Te enviamos un correo con instrucciones para restablecer tu contraseña.
                </Text>
              )}
              {!!error && (
                <Text className="mt-2 text-sm text-red-500 text-center">
                  {error}
                </Text>
              )}

              {/* Botón enviar */}
              <Pressable
                className={`mt-4 rounded-full p-4 ${disabled ? 'bg-gray-300' : 'bg-[#0071CE]'}`}
                android_ripple={{ color: '#ffffff22' }}
                onPress={onSubmit}
                disabled={disabled}
                style={style.shadow}
              >
                {sending ? (
                  <ActivityIndicator />
                ) : (
                  <Text className="text-center font-bold text-white">
                    Enviar instrucciones
                  </Text>
                )}
              </Pressable>

              {/* Volver a Login */}
              <View className="mt-4 w-full">
                <Pressable
                  style={style.shadow}
                  className="group rounded-full bg-white p-4 active:bg-[#0071CE]"
                  onPress={() => router.replace('/(auth)')}
                >
                  <Text className="text-center font-bold text-[#0071CE] group-active:text-white">
                    Volver a iniciar sesión
                  </Text>
                </Pressable>
              </View>

              {/* Texto auxiliar */}
              <Text className="text-xs text-gray-400 text-center mt-2">
                Si no ves el correo, revisa tu carpeta de spam o espera unos minutos.
              </Text>
            </View>
          </View>
        </SafeAreaView>
      </KeyboardAwareScrollView>

      <KeyboardToolbar />
    </>
  );
}

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