// app/(auth)/Register.tsx
import React, { useMemo, useState } from 'react';
import { View, Text, Image, TextInput, Pressable, ActivityIndicator } from 'react-native';
import {
  KeyboardAwareScrollView,
  KeyboardToolbar,
} from 'react-native-keyboard-controller';
import { SafeAreaView } from 'react-native-safe-area-context';
import { MaterialIcons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { useAuth } from '~/src/features/auth/presentation/providers/AuthProvider';

type RegisterResult =
  | { ok: true; user: any }
  | { ok: false; message: string };

type RegisterFormProps = {
  onSuccess: (user: any) => void;
};

function RegisterForm({ onSuccess }: RegisterFormProps) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [pass, setPass] = useState('');
  const [confirm, setConfirm] = useState('');
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  const disabled = useMemo(() => {
    if (loading) return true;
    if (!email || !pass || !confirm) return true;
    if (pass.length < 6) return true;
    if (pass !== confirm) return true;
    // Validación simple de email
    const re = /\S+@\S+\.\S+/;
    if (!re.test(email)) return true;
    return false;
  }, [email, pass, confirm, loading]);

  const doRegister = async (): Promise<RegisterResult> => {
    // TODO: Reemplaza este stub por tu llamada real de API.
    // La idea es que devuelvas { ok: true, user } cuando el backend cree la cuenta.
    // Aquí simulamos éxito tras 900ms.
    await new Promise((r) => setTimeout(r, 900));
    // Simulación de "usuario" retornado por backend
    return {
      ok: true,
      user: {
        id: Date.now().toString(),
        name: name || email.split('@')[0],
        email,
      },
    };
  };

  const onSubmit = async () => {
    setErr(null);
    setLoading(true);
    try {
      const res = await doRegister();
      if (res.ok) {
        onSuccess(res.user);
      } else {
        setErr(res.message || 'No se pudo crear la cuenta.');
      }
    } catch (e: any) {
      setErr(e?.message ?? 'Ha ocurrido un error inesperado.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <View className="w-full flex-col gap-3">
      {/* Nombre opcional */}
      <View className="flex-row items-center gap-3 bg-white rounded-2xl px-4 py-3 border border-gray-200">
        <MaterialIcons name="person" size={22} color="gray" />
        <TextInput
          className="flex-1 text-base text-gray-800"
          placeholder="Usuario"
          placeholderTextColor="#9CA3AF"
          value={name}
          onChangeText={setName}
          autoCapitalize="words"
          returnKeyType="next"
        />
      </View>

      {/* Email */}
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
          returnKeyType="next"
        />
      </View>

      {/* Contraseña */}
      <View className="flex-row items-center gap-3 bg-white rounded-2xl px-4 py-3 border border-gray-200">
        <MaterialIcons name="lock" size={22} color="gray" />
        <TextInput
          className="flex-1 text-base text-gray-800"
          placeholder="Contraseña (mín. 6 caracteres)"
          placeholderTextColor="#9CA3AF"
          value={pass}
          onChangeText={setPass}
          secureTextEntry
          autoCapitalize="none"
          returnKeyType="next"
        />
      </View>

      {/* Confirmar contraseña */}
      <View className="flex-row items-center gap-3 bg-white rounded-2xl px-4 py-3 border border-gray-200">
        <MaterialIcons name="lock-outline" size={22} color="gray" />
        <TextInput
          className="flex-1 text-base text-gray-800"
          placeholder="Confirmar contraseña"
          placeholderTextColor="#9CA3AF"
          value={confirm}
          onChangeText={setConfirm}
          secureTextEntry
          autoCapitalize="none"
          returnKeyType="done"
          onSubmitEditing={() => {
            if (!disabled) onSubmit();
          }}
        />
      </View>

      {/* Mensaje de error */}
      {!!err && (
        <Text className="text-red-500 text-sm mt-1">
          {err}
        </Text>
      )}

      {/* Botón crear cuenta */}
      <Pressable
        className={`mt-2 rounded-full p-4 ${disabled ? 'bg-gray-300' : 'bg-[#0071CE]'}`}
        android_ripple={{ color: '#ffffff22' }}
        onPress={onSubmit}
        disabled={disabled}
        style={style.shadow}
      >
        {loading ? (
          <ActivityIndicator />
        ) : (
          <Text className="text-center font-bold text-white">Crear cuenta</Text>
        )}
      </Pressable>

      <Text className="text-xs text-gray-400 text-center mt-1">
        Al registrarte aceptas los Términos y la Política de Privacidad.
      </Text>
    </View>
  );
}

export const RegisterScreen = () => {
  const router = useRouter();
  const { signIn } = useAuth(); // reutilizamos el onSuccess para autenticar tras crear la cuenta

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
                Crear cuenta
              </Text>

              {/* Formulario de registro */}
              <RegisterForm onSuccess={signIn} />

              {/* Ir a Login */}
              <View className="mt-4 w-full">
                <Pressable
                  style={style.shadow}
                  className="group rounded-full bg-white p-4 active:bg-[#0071CE]"
                  onPress={() => router.replace('/(auth)')}
                >
                  <Text className="text-center font-bold text-[#0071CE] group-active:text-white">
                    ¿Ya tienes cuenta? Inicia sesión
                  </Text>
                </Pressable>
              </View>
            </View>
          </View>
        </SafeAreaView>
      </KeyboardAwareScrollView>

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

export default RegisterScreen;