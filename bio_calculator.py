import streamlit as st

# Конфигурация страницы
st.set_page_config(
    page_title="Калькулятор разведений",
    page_icon="",
    layout="centered"
)

# Стилизация результатов
st.markdown("""
<style>
    .header { color: #1e3a8a; font-weight: 700; }
    .result { 
        background-color: #111; 
        color: #ffffff; 
        padding: 15px; 
        border-radius: 10px; 
    }
    .unit-box { background-color: #eff6ff; padding: 5px 10px; border-radius: 5px; }
    .dark-text { color: #ffffff; }
</style>
""", unsafe_allow_html=True)

# Заголовок
st.title("Калькулятор разведений")


# Основные единицы измерения
CONCENTRATION_UNITS = ["мкг/мл", "мг/мл", "г/л", "мМ", "нМ", "%"]
VOLUME_UNITS = ["мл", "л", "мкл"]

# Выбор типа расчета
calc_type = st.radio("**Тип расчета:**", [
    " Определить объем исходного раствора",
    " Определить конечную концентрацию"
], index=0)

# Основная форма
with st.form(key='dilution_form'):
    col1, col2 = st.columns(2)
    
    if "объем" in calc_type:
        # Режим 1: Расчет объема исходного раствора
        with col1:
            c1 = st.number_input("Концентрация исходного раствора (C₁)", min_value=0.001, value=1.0, step=0.1)
            c1_unit = st.selectbox("Единицы C₁", CONCENTRATION_UNITS, index=1)
            
        with col2:
            c2 = st.number_input("Желаемая концентрация (C₂)", min_value=0.001, value=0.1, step=0.01)
            c2_unit = st.selectbox("Единицы C₂", CONCENTRATION_UNITS, index=1)
            v2 = st.number_input("Желаемый конечный объем (V₂)", min_value=0.001, value=10.0, step=0.1)
            v2_unit = st.selectbox("Единицы V₂", VOLUME_UNITS, index=0)
    else:
        # Режим 2: Расчет конечной концентрации
        with col1:
            c1 = st.number_input("Концентрация исходного раствора (C₁)", min_value=0.001, value=1.0, step=0.1)
            c1_unit = st.selectbox("Единицы C₁", CONCENTRATION_UNITS, index=1)
            v1 = st.number_input("Объем исходного раствора (V₁)", min_value=0.001, value=1.0, step=0.1)
            v1_unit = st.selectbox("Единицы V₁", VOLUME_UNITS, index=0)
            
        with col2:
            v2 = st.number_input("Конечный объем (V₂)", min_value=0.001, value=10.0, step=0.1)
            v2_unit = st.selectbox("Единицы V₂", VOLUME_UNITS, index=0)

    # Кнопка расчета
    submitted = st.form_submit_button("Рассчитать", use_container_width=True)

# Блок результатов
if submitted:
    st.divider()
    st.subheader(" Результаты расчета")
    
    try:
        if "объем" in calc_type:
            # Проверка совпадения единиц
            if c1_unit != c2_unit:
                st.warning("⚠️ Единицы концентраций не совпадают! Результат может быть некорректен.")
            
            # Основная формула: V1 = (C2 * V2) / C1
            v1 = (c2 * v2) / c1
            
            # Автоконвертация для маленьких объемов
            result_unit = v2_unit
            if v1 < 0.1 and v2_unit == "мл":
                v1 *= 1000
                result_unit = "мкл"
            elif v1 < 0.001 and v2_unit == "мл":
                v1 *= 1000000
                result_unit = "нл"
                
            st.markdown(f"""
            <div class="result">
                <b>Объем исходного раствора:</b> {v1:.4f} {result_unit}<br>
                <b>Объем растворителя:</b> {v2 - v1:.2f} {v2_unit}
            </div>
            """, unsafe_allow_html=True)
            
            # Протокол приготовления
            st.markdown('<p class="dark-text">Протокол:</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="dark-text">1. Влейте {v1:.2f} {result_unit} исходного раствора в мерную колбу</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="dark-text">2. Добавьте растворитель до общего объема {v2} {v2_unit}</p>', unsafe_allow_html=True)
            
        else:
            # Расчет конечной концентрации: C2 = (C1 * V1) / V2
            c2 = (c1 * v1) / v2
            
            # Автовыбор единиц для маленьких концентраций
            result_unit = c1_unit
            if c2 < 0.001 and "м" in c1_unit:
                c2 *= 1000
                result_unit = "μ" + c1_unit[1:]  # Заменяем префикс
            
            st.markdown(f"""
            <div class="result">
                <b>Конечная концентрация:</b> {c2:.4g} {result_unit}
            </div>
            """, unsafe_allow_html=True)
            
            # Дополнительная информация
            dilution_factor = v2 / v1
            st.markdown(f'<p class="dark-text">Коэффициент разведения: 1:{dilution_factor:.1f}</p>', unsafe_allow_html=True)
    
    except ZeroDivisionError:
        st.error("Ошибка: Нулевые значения недопустимы!")

# Информационная панель
st.divider()
st.markdown("""
**💡 Как использовать:**
1. Выберите тип расчета
2. Введите параметры растворов
3. Нажмите "Рассчитать"
4. Используйте результаты в протоколе""")
