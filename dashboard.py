import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def main():
    # Чтение CSV файлов с обработкой ошибок
    try:
        # Читаем файл с лидами
        leads_df = pd.read_csv('leads2025.csv')
        st.success(f"✅ Файл leads2025.csv успешно загружен! Размер: {leads_df.shape[0]} строк, {leads_df.shape[1]} столбцов")
        
    except FileNotFoundError:
        st.error("❌ Файл leads2025.csv не найден!")
        leads_df = None
    except Exception as e:
        st.error(f"❌ Ошибка при чтении файла leads2025.csv: {str(e)}")
        leads_df = None

    try:
        # Читаем файл с покупками
        purchases_df = pd.read_csv('purchases2025.csv')
        st.success(f"✅ Файл purchases2025.csv успешно загружен! Размер: {purchases_df.shape[0]} строк, {purchases_df.shape[1]} столбцов")
        
    except FileNotFoundError:
        st.error("❌ Файл purchases2025.csv не найден!")
        purchases_df = None
    except Exception as e:
        st.error(f"❌ Ошибка при чтении файла purchases2025.csv: {str(e)}")
        purchases_df = None

    try:
        # Читаем файл с данными Яндекс.Метрики
        ymetrica_df = pd.read_csv('YMetrica.csv')
        st.success(f"✅ Файл YMetrica.csv успешно загружен! Размер: {ymetrica_df.shape[0]} строк, {ymetrica_df.shape[1]} столбцов")
        
    except FileNotFoundError:
        st.error("❌ Файл YMetrica.csv не найден!")
        ymetrica_df = None
    except Exception as e:
        st.error(f"❌ Ошибка при чтении файла YMetrica.csv: {str(e)}")
        ymetrica_df = None

    try:
        # Читаем файл с активациями с автоматическим определением разделителя
        activations_df = pd.read_csv('Активации 1.01-1.04.csv', sep=None, engine='python', encoding='utf-8')
        st.success(f"✅ Файл Активации 1.01-1.04.csv успешно загружен! Размер: {activations_df.shape[0]} строк, {activations_df.shape[1]} столбцов")
        
    except FileNotFoundError:
        st.error("❌ Файл Активации 1.01-1.04.csv не найден!")
        activations_df = None
    except Exception as e:
        st.error(f"❌ Ошибка при чтении файла Активации 1.01-1.04.csv: {str(e)}")
        # Пробуем альтернативные способы чтения
        try:
            st.info("🔄 Пробуем альтернативные способы чтения файла...")
            # Пробуем с разными разделителями
            for sep in [',', ';', '\t', '|']:
                try:
                    activations_df = pd.read_csv('Активации 1.01-1.04.csv', sep=sep, encoding='utf-8')
                    st.success(f"✅ Файл успешно прочитан с разделителем '{sep}'! Размер: {activations_df.shape[0]} строк, {activations_df.shape[1]} столбцов")
                    break
                except:
                    continue
            
            if activations_df is None:
                # Пробуем с автоматическим определением кодировки
                try:
                    activations_df = pd.read_csv('Активации 1.01-1.04.csv', sep=None, engine='python', encoding='latin-1')
                    st.success(f"✅ Файл успешно прочитан с кодировкой latin-1! Размер: {activations_df.shape[0]} строк, {activations_df.shape[1]} столбцов")
                except:
                    st.error("❌ Не удалось прочитать файл ни одним из способов")
                    activations_df = None
                    
        except Exception as e2:
            st.error(f"❌ Все попытки чтения файла не удались: {str(e2)}")
            activations_df = None

    # Проверяем, что основные файлы загружены успешно
    if leads_df is not None and purchases_df is not None and ymetrica_df is not None:
        st.success("🎉 Все файлы успешно загружены!")
        
        # Показываем краткую информацию о данных
        st.subheader("📊 Краткая информация о данных:")
        
        # Диагностика файла активаций
        if activations_df is not None:
            st.info("🔍 Диагностика файла активаций:")
            st.write(f"**Колонки:** {list(activations_df.columns)}")
            st.write(f"**Типы данных:** {activations_df.dtypes.to_dict()}")
            st.write("**Первые 5 строк:**")
            st.dataframe(activations_df.head(), use_container_width=True)
            
            # Детальная диагностика для столбца "ID Устройства"
            st.info("🔍 Детальная диагностика столбца 'ID Устройства':")
            
            # Проверяем точное название столбца
            device_id_found = False
            for col in activations_df.columns:
                if 'ID' in col and 'Устройства' in col:
                    st.success(f"✅ Найден столбец: '{col}' (содержит 'ID' и 'Устройства')")
                    device_id_found = True
                    device_id_count = activations_df[col].notna().sum()
                    device_id_unique = activations_df[col].nunique()
                    st.info(f"📊 В столбце '{col}': {device_id_count} непустых значений, {device_id_unique} уникальных значений")
                    break
            
            if not device_id_found:
                st.warning("⚠️ Столбец 'ID Устройства' НЕ найден в файле активаций")
                st.info("🔍 Доступные столбцы:")
                for i, col in enumerate(activations_df.columns, 1):
                    st.write(f"   {i}. '{col}' (длина: {len(col)})")
                    
                # Ищем похожие столбцы
                similar_columns = []
                for col in activations_df.columns:
                    if 'id' in col.lower() or 'устройства' in col.lower():
                        similar_columns.append(col)
                
                if similar_columns:
                    st.info(f"🔍 Похожие столбцы: {similar_columns}")
        else:
            st.warning("⚠️ Файл активаций не загружен - диагностика невозможна")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Лиды", f"{leads_df.shape[0]:,}")
            st.metric("Столбцы лидов", leads_df.shape[1])
            
        with col2:
            st.metric("Покупки", f"{purchases_df.shape[0]:,}")
            st.metric("Столбцы покупок", purchases_df.shape[1])
            
        with col3:
            st.metric("События YM", f"{ymetrica_df.shape[0]:,}")
            st.metric("Столбцы YM", ymetrica_df.shape[1])
            
        with col4:
            if activations_df is not None:
                st.metric("Активации", f"{activations_df.shape[0]:,}")
                st.metric("Столбцы активаций", activations_df.shape[1])
            else:
                st.metric("Активации", "Не загружен")
                st.metric("Столбцы активаций", "N/A")
        
        # ТАБЛИЦА 1: Аналитика лидов по месяцам (только из leads2025)
        st.subheader("📊 ТАБЛИЦА 1: Аналитика лидов по месяцам")
        
        try:
            # Создаем аналитическую таблицу на основе всех лидов из leads2025
            st.info("📋 Создаем аналитическую таблицу на основе всех лидов из leads2025...")
            
            # Берем все лиды из leads2025
            leads_analysis = leads_df.copy()
            
            # Шаг 1: Находим совпадения с YMetrica для определения источника трафика
            st.info("🔍 Определяем источники трафика для лидов...")
            try:
                # Инициализация столбца по умолчанию
                leads_analysis['Источник трафика'] = 'Неизвестен'
                
                # Проверяем наличие необходимых столбцов
                if 'ClientID' not in ymetrica_df.columns:
                    st.warning("⚠️ В YMetrica отсутствует столбец 'ClientID'. Все источники помечены как 'Неизвестен'.")
                elif 'firstTrafficSource' not in ymetrica_df.columns:
                    st.warning("⚠️ В YMetrica отсутствует столбец 'firstTrafficSource'. Все источники помечены как 'Неизвестен'.")
                else:
                    # Функция нормализации идентификаторов: обрезаем пробелы, убираем .0 и неалфанум символы
                    def _normalize(series):
                        return (
                            series.astype(str)
                            .str.strip()
                            .str.replace(r'\\.0$', '', regex=True)
                            .str.replace(r'[^0-9A-Za-z]+', '', regex=True)
                            .str.lower()
                        )
                    
                    # Нормализуем идентификаторы в YMetrica
                    ym_map_df = pd.DataFrame({
                        'ClientID_norm': _normalize(ymetrica_df['ClientID']),
                        'firstTrafficSource': ymetrica_df['firstTrafficSource']
                    })
                    ym_map_df = ym_map_df.dropna(subset=['ClientID_norm'])
                    ym_map_df = ym_map_df[ym_map_df['ClientID_norm'].str.len() > 0]
                    ym_map_df = ym_map_df.drop_duplicates(subset=['ClientID_norm'], keep='first')
                    ym_mapping = dict(zip(ym_map_df['ClientID_norm'], ym_map_df['firstTrafficSource']))
                    
                    # Определяем имена столбцов в leads (поддержка альтернативных имен)
                    yclid_col = 'Yclid' if 'Yclid' in leads_analysis.columns else ('yclid' if 'yclid' in leads_analysis.columns else None)
                    ymuid_col = '_ym_uid' if '_ym_uid' in leads_analysis.columns else ('ym_uid' if 'ym_uid' in leads_analysis.columns else None)
                    
                    # Нормализуем идентификаторы в leads
                    leads_analysis['Yclid_norm'] = _normalize(leads_analysis[yclid_col]) if yclid_col else ''
                    leads_analysis['_ym_uid_norm'] = _normalize(leads_analysis[ymuid_col]) if ymuid_col else ''
                    
                    # Диагностика перекрытий
                    ym_clientids = ym_map_df['ClientID_norm']
                    yclid_nonempty_unique = leads_analysis.loc[leads_analysis['Yclid_norm'] != '', 'Yclid_norm'].nunique()
                    ymuid_nonempty_unique = leads_analysis.loc[leads_analysis['_ym_uid_norm'] != '', '_ym_uid_norm'].nunique()
                    ym_unique = ym_clientids.nunique()
                    overlap_yclid = leads_analysis['Yclid_norm'].isin(ym_clientids.values).sum()
                    overlap_ymuid = leads_analysis['_ym_uid_norm'].isin(ym_clientids.values).sum()
                    st.info(f"Yclid уникальных (не пустых): {yclid_nonempty_unique}, _ym_uid уникальных (не пустых): {ymuid_nonempty_unique}, YM ClientID уникальных: {ym_unique}, пересечений Yclid↔ClientID: {overlap_yclid}, пересечений _ym_uid↔ClientID: {overlap_ymuid}")
                    
                    # Сопоставляем источники: сначала по Yclid, затем по _ym_uid
                    yclid_sources = leads_analysis['Yclid_norm'].map(ym_mapping)
                    ymuid_sources = leads_analysis['_ym_uid_norm'].map(ym_mapping)
                    final_sources = yclid_sources.fillna(ymuid_sources)
                    
                    # Применяем источники в таблицу лидов
                    leads_analysis.loc[final_sources.notna(), 'Источник трафика'] = final_sources[final_sources.notna()]
                    
                    # Подсчет статистики
                    matched_by_yclid = int((yclid_sources.notna()).sum())
                    matched_by_ym_uid = int(((yclid_sources.isna()) & (ymuid_sources.notna())).sum())
                    unmatched = int((leads_analysis['Источник трафика'] == 'Неизвестен').sum())
                    
                    st.success(f"✅ Источники трафика определены: по Yclid - {matched_by_yclid}, по _ym_uid - {matched_by_ym_uid}, неизвестно - {unmatched}")
            except Exception as e:
                st.error(f"❌ Ошибка при определении источников трафика: {str(e)}")
            
            # Обрабатываем столбец 'Дата создания'
            if 'Дата создания' in leads_analysis.columns:
                # Конвертируем в datetime и извлекаем месяц
                leads_analysis['Дата создания'] = pd.to_datetime(leads_analysis['Дата создания'], errors='coerce')
                leads_analysis['Месяц'] = leads_analysis['Дата создания'].dt.to_period('M')
                
                # Убираем строки без даты
                leads_analysis_clean = leads_analysis[leads_analysis['Месяц'].notna()].copy()
                
                if len(leads_analysis_clean) > 0:
                    # Создаем аналитическую таблицу по месяцам И источникам трафика
                    if 'Этап сделки' in leads_analysis_clean.columns:
                        # Группируем по месяцу и источнику трафика
                        analytics_df = leads_analysis_clean.groupby(['Месяц', 'Источник трафика']).agg({
                            'ID': 'count',  # Количество лидов по месяцам и источникам
                        }).rename(columns={
                            'ID': 'Количество лидов'
                        }).reset_index()
                        
                        # ===== УСЛОЖНЕННАЯ ЛОГИКА СТОЛБЦА "НОВЫЕ АКТИВАЦИИ ТСД" =====
                        st.info("🔍 Создаем столбец 'Новые активации ТСД' с усложненной логикой...")
                        
                        # Проверяем наличие необходимых столбцов в файле активаций
                        if activations_df is not None:
                            required_columns = ['Счет', 'Первая активация']
                            missing_columns = [col for col in required_columns if col not in activations_df.columns]
                            if missing_columns:
                                st.warning(f"⚠️ В файле активаций отсутствуют столбцы: {', '.join(missing_columns)}")
                            
                            # Проверяем наличие столбца "ID Устройства" для учета дублей
                            device_id_column = None
                            for col in activations_df.columns:
                                if 'ID' in col and 'Устройства' in col:
                                    device_id_column = col
                                    break
                            
                            if device_id_column:
                                st.info(f"✅ Столбец '{device_id_column}' найден - будет учитываться при подсчете дублей")
                            else:
                                st.warning("⚠️ Столбец 'ID Устройства' отсутствует - дубли по устройствам учитываться не будут")
                        else:
                            st.warning("⚠️ Файл активаций не загружен - проверка столбцов невозможна")
                        
                        # 1. Создаем столбец "Новые активации ТСД" и инициализируем нулями
                        analytics_df['Новые активации ТСД'] = 0
                        
                        # 2. Получаем данные из purchases2025 - столбец "Номер счета 1С"
                        if 'Номер счета 1С' in purchases_df.columns:
                            purchase_accounts = purchases_df['Номер счета 1С'].dropna().astype(str).unique()
                            st.info(f"📊 Найдено {len(purchase_accounts)} уникальных номеров счетов 1С в purchases2025")
                        else:
                            st.warning("⚠️ В purchases2025 отсутствует столбец 'Номер счета 1С'")
                            purchase_accounts = []
                        
                        # 3. Получаем данные из "Активации 1.01-1.04" - столбец "Счет" с учетом "Первая активация"
                        if activations_df is not None and 'Счет' in activations_df.columns:
                            # Фильтруем только строки где "Первая активация" не пустая
                            if 'Первая активация' in activations_df.columns:
                                # Создаем маску для непустых значений в "Первая активация"
                                first_activation_mask = activations_df['Первая активация'].notna() & (activations_df['Первая активация'] != '')
                                
                                # Применяем фильтр
                                filtered_activations = activations_df[first_activation_mask]
                                st.info(f"📊 Применен фильтр 'Первая активация' не пустая: {len(filtered_activations)} из {len(activations_df)} строк")
                                
                                # Получаем уникальные номера счетов с учетом дублей по "ID Устройства"
                                device_id_column = None
                                for col in activations_df.columns:
                                    if 'ID' in col and 'Устройства' in col:
                                        device_id_column = col
                                        break
                                
                                if device_id_column:
                                    # Каждая уникальная комбинация "счет + ID устройства" считается как отдельная активация
                                    # Создаем уникальные комбинации счетов и устройств
                                    unique_combinations = filtered_activations[['Счет', device_id_column]].drop_duplicates()
                                    activation_accounts = unique_combinations['Счет'].dropna().astype(str).unique()
                                    st.info(f"📊 Найдено {len(activation_accounts)} уникальных номеров счетов")
                                    st.info(f"📊 Общее количество уникальных комбинаций 'счет + устройство': {len(unique_combinations)}")
                                else:
                                    # Если нет столбца "ID Устройства", просто берем уникальные счета
                                    activation_accounts = filtered_activations['Счет'].dropna().astype(str).unique()
                                    st.info(f"📊 Найдено {len(activation_accounts)} уникальных номеров счетов (столбец 'ID Устройства' отсутствует)")
                            else:
                                st.warning("⚠️ В файле активаций отсутствует столбец 'Первая активация'")
                                activation_accounts = []
                        else:
                            st.warning("⚠️ Файл активаций не загружен или отсутствует столбец 'Счет'")
                            activation_accounts = []
                        
                        # 4. Сравниваем данные и находим совпадения
                        if len(purchase_accounts) > 0 and len(activation_accounts) > 0:
                            # Преобразуем в множества для быстрого поиска
                            purchase_set = set(purchase_accounts)
                            activation_set = set(activation_accounts)
                            
                            # Находим совпадения
                            matching_accounts = purchase_set.intersection(activation_set)
                            st.info(f"🔍 Найдено {len(matching_accounts)} совпадающих номеров счетов")
                            
                            # Дополнительная диагностика
                            st.info(f"📊 Детализация:")
                            st.info(f"   • Номеров счетов в purchases2025: {len(purchase_set)}")
                            st.info(f"   • Номеров счетов в активациях (с фильтром): {len(activation_set)}")
                            st.info(f"   • Совпадающих номеров: {len(matching_accounts)}")
                            
                            # Показываем примеры совпадающих счетов
                            if len(matching_accounts) > 0:
                                sample_accounts = list(matching_accounts)[:5]  # Первые 5 для примера
                                st.info(f"   • Примеры совпадающих счетов: {', '.join(sample_accounts)}")
                            
                            if len(matching_accounts) > 0:
                                # 5. Заполняем столбец "Новые активации ТСД" количеством совпадений по месяцам
                                st.info("📝 Заполняем столбец 'Новые активации ТСД'...")
                                
                                # Создаем словарь для подсчета активаций по месяцам и источникам
                                activations_by_month_source = {}
                                
                                # Проходим по всем лидам и ищем совпадения
                                for _, lead in leads_analysis_clean.iterrows():
                                    lead_month = lead['Месяц']
                                    lead_source = lead['Источник трафика']
                                    key = (lead_month, lead_source)
                                    
                                    if key not in activations_by_month_source:
                                        activations_by_month_source[key] = 0
                                    
                                    # Ищем покупки по этому лиду
                                    found_activation = False
                                    
                                                                        # Проверяем по ClientID
                                    if pd.notna(lead['ClientID']) and lead['ClientID'] != '':
                                        lead_purchases = purchases_df[purchases_df['ClientID'] == lead['ClientID']]
                                        for _, purchase in lead_purchases.iterrows():
                                            if pd.notna(purchase['Номер счета 1С']):
                                                purchase_account = str(purchase['Номер счета 1С'])
                                                if purchase_account in matching_accounts:
                                                    # Если есть столбец ID Устройства, считаем каждую уникальную комбинацию
                                                    if device_id_column:
                                                        # Находим все активации для этого счета
                                                        account_activations = filtered_activations[filtered_activations['Счет'] == purchase_account]
                                                        # Считаем количество уникальных устройств для этого счета
                                                        unique_devices = account_activations[device_id_column].nunique()
                                                        activations_by_month_source[key] += unique_devices
                                                    else:
                                                        # Если нет столбца ID Устройства, считаем как 1
                                                        activations_by_month_source[key] += 1
                                                    found_activation = True
                                                    break
                                    
                                    # Если не нашли по ClientID, проверяем по Yclid
                                    if not found_activation and pd.notna(lead['Yclid']) and lead['Yclid'] != '':
                                        lead_purchases = purchases_df[purchases_df['Yclid'] == lead['Yclid']]
                                        for _, purchase in lead_purchases.iterrows():
                                            if pd.notna(purchase['Номер счета 1С']):
                                                purchase_account = str(purchase['Номер счета 1С'])
                                                if purchase_account in matching_accounts:
                                                    # Если есть столбец ID Устройства, считаем каждую уникальную комбинацию
                                                    if device_id_column:
                                                        # Находим все активации для этого счета
                                                        account_activations = filtered_activations[filtered_activations['Счет'] == purchase_account]
                                                        # Считаем количество уникальных устройств для этого счета
                                                        unique_devices = account_activations[device_id_column].nunique()
                                                        activations_by_month_source[key] += unique_devices
                                                    else:
                                                        # Если нет столбца ID Устройства, считаем как 1
                                                        activations_by_month_source[key] += 1
                                                    found_activation = True
                                                    break
                                    
                                    # Если не нашли по Yclid, проверяем по _ym_uid
                                    if not found_activation and pd.notna(lead['_ym_uid']) and lead['_ym_uid'] != '':
                                        lead_purchases = purchases_df[purchases_df['_ym_uid'] == lead['Yclid']]
                                        for _, purchase in lead_purchases.iterrows():
                                            if pd.notna(purchase['Номер счета 1С']):
                                                purchase_account = str(purchase['Номер счета 1С'])
                                                if purchase_account in matching_accounts:
                                                    # Если есть столбец ID Устройства, считаем каждую уникальную комбинацию
                                                    if device_id_column:
                                                        # Находим все активации для этого счета
                                                        account_activations = filtered_activations[filtered_activations['Счет'] == purchase_account]
                                                        # Считаем количество уникальных устройств для этого счета
                                                        unique_devices = account_activations[device_id_column].nunique()
                                                        activations_by_month_source[key] += unique_devices
                                                    else:
                                                        # Если нет столбца ID Устройства, считаем как 1
                                                        activations_by_month_source[key] += 1
                                                    found_activation = True
                                                    break
                                
                                # Обновляем столбец "Новые активации ТСД" в analytics_df
                                for (month, source), count in activations_by_month_source.items():
                                    mask = (analytics_df['Месяц'] == month) & (analytics_df['Источник трафика'] == source)
                                    analytics_df.loc[mask, 'Новые активации ТСД'] = count
                                
                                total_new_activations = sum(activations_by_month_source.values())
                                st.success(f"✅ Столбец 'Новые активации ТСД' заполнен! Найдено {total_new_activations} новых активаций")
                            else:
                                st.info("ℹ️ Совпадающих номеров счетов не найдено")
                                total_new_activations = 0
                        else:
                            st.warning("⚠️ Недостаточно данных для анализа новых активаций ТСД")
                            total_new_activations = 0
                        
                        # ===== КОНЕЦ НОВОЙ ЛОГИКИ =====
                    
                        # Создаем маску для предквалифицированных лидов
                        prequalified_mask = leads_analysis_clean['Этап сделки'] == 'Лид предквалифицирован'
                        
                        # Группируем предквалифицированные лиды по месяцам и источникам
                        prequalified_by_month_source = leads_analysis_clean[prequalified_mask].groupby(['Месяц', 'Источник трафика'])['ID'].count().reset_index()
                        prequalified_by_month_source = prequalified_by_month_source.rename(columns={'ID': 'Предквалифицированные лиды'})
                        
                        # Объединяем основную таблицу с предквалифицированными лидами
                        analytics_df = analytics_df.merge(
                            prequalified_by_month_source,
                            on=['Месяц', 'Источник трафика'],
                            how='left'
                        )
                        
                        # Заполняем NaN значения нулями
                        analytics_df['Предквалифицированные лиды'] = analytics_df['Предквалифицированные лиды'].fillna(0).astype(int)
                        
                        # Убеждаемся, что столбец "Новые активации ТСД" существует
                        if 'Новые активации ТСД' not in analytics_df.columns:
                            analytics_df['Новые активации ТСД'] = 0
                        
                        # Добавляем столбец конверсии в предквалификацию
                        analytics_df['Конверсия в предквалификацию (%)'] = (
                            (analytics_df['Предквалифицированные лиды'] / analytics_df['Количество лидов'] * 100)
                            .round(2)
                        )
                        
                        # Сортируем по месяцам
                        analytics_df = analytics_df.sort_values(['Месяц', 'Источник трафика'])
                        
                        # Добавляем столбец "Купили" - кто из предквалифицированных лидов в итоге купил
                        st.info("🔍 Анализируем покупки среди предквалифицированных лидов...")
                        
                        # Оптимизация: работаем только с предквалифицированными лидами для экономии памяти
                        prequalified_leads = leads_analysis_clean[leads_analysis_clean['Этап сделки'] == 'Лид предквалифицирован'].copy()
                        
                        if len(prequalified_leads) > 0:
                            st.info(f"📊 Найдено {len(prequalified_leads)} предквалифицированных лидов для анализа покупок")
                            
                            # Создаем DataFrame для хранения результатов по месяцам и источникам трафика
                            purchased_results = []
                            
                            # Создаем множество для отслеживания уже учтенных контактов
                            processed_contacts = set()
                            
                            # Анализируем каждый месяц и источник трафика отдельно для экономии памяти
                            for (month, source) in prequalified_leads[['Месяц', 'Источник трафика']].drop_duplicates().values:
                                month_source_leads = prequalified_leads[
                                    (prequalified_leads['Месяц'] == month) & 
                                    (prequalified_leads['Источник трафика'] == source)
                                ]
                                purchased_count = 0
                                
                                # Для каждого лида в месяце ищем покупки
                                for _, lead in month_source_leads.iterrows():
                                    found_purchase = False
                                    
                                    # Создаем уникальный идентификатор контакта для проверки дубликатов
                                    contact_key = None
                                    
                                    # Определяем ключ контакта (приоритет: ClientID > Yclid > _ym_uid > Основной контакт)
                                    if pd.notna(lead['ClientID']) and lead['ClientID'] != '':
                                        contact_key = f"ClientID_{lead['ClientID']}"
                                    elif pd.notna(lead['Yclid']) and lead['Yclid'] != '':
                                        contact_key = f"Yclid_{lead['Yclid']}"
                                    elif pd.notna(lead['_ym_uid']) and lead['_ym_uid'] != '':
                                        contact_key = f"_ym_uid_{lead['_ym_uid']}"
                                    elif pd.notna(lead['Основной контакт']) and lead['Основной контакт'] != '':
                                        contact_key = f"Contact_{lead['Основной контакт']}"
                                    
                                    # Проверяем, не обрабатывали ли мы уже этот контакт
                                    if contact_key is None or contact_key in processed_contacts:
                                        continue
                                    
                                    # Получаем дату создания лида
                                    lead_date = lead['Дата создания']
                                    
                                    # 1. Ищем по ClientID
                                    if pd.notna(lead['ClientID']) and lead['ClientID'] != '':
                                        # Отбираем только покупки со статусом "Успешно реализовано"
                                        successful_purchases = purchases_df[
                                            (purchases_df['ClientID'] == lead['ClientID']) & 
                                            (purchases_df['Этап сделки'] == 'Успешно реализовано')
                                        ]
                                        
                                        # Проверяем, что есть покупки с датой закрытия после даты создания лида
                                        for _, purchase in successful_purchases.iterrows():
                                            if pd.notna(purchase['Дата закрытия']):
                                                purchase_date = pd.to_datetime(purchase['Дата закрытия'], errors='coerce')
                                                if pd.notna(purchase_date) and purchase_date > lead_date:
                                                    purchased_count += 1
                                                    found_purchase = True
                                                    processed_contacts.add(contact_key)  # Отмечаем контакт как обработанный
                                                    break  # Нашли покупку, прекращаем поиск
                                    
                                    # 2. Если не нашли по ClientID, ищем по Yclid
                                    if not found_purchase and pd.notna(lead['Yclid']) and lead['Yclid'] != '':
                                        successful_purchases = purchases_df[
                                            (purchases_df['Yclid'] == lead['Yclid']) & 
                                            (purchases_df['Этап сделки'] == 'Успешно реализовано')
                                        ]
                                        
                                        for _, purchase in successful_purchases.iterrows():
                                            if pd.notna(purchase['Дата закрытия']):
                                                purchase_date = pd.to_datetime(purchase['Дата закрытия'], errors='coerce')
                                                if pd.notna(purchase_date) and purchase_date > lead_date:
                                                    purchased_count += 1
                                                    found_purchase = True
                                                    processed_contacts.add(contact_key)  # Отмечаем контакт как обработанный
                                                    break
                                    
                                    # 3. Если не нашли по Yclid, ищем по _ym_uid
                                    if not found_purchase and pd.notna(lead['_ym_uid']) and lead['_ym_uid'] != '':
                                        successful_purchases = purchases_df[
                                            (purchases_df['_ym_uid'] == lead['_ym_uid']) & 
                                            (purchases_df['Этап сделки'] == 'Успешно реализовано')
                                        ]
                                        
                                        for _, purchase in successful_purchases.iterrows():
                                            if pd.notna(purchase['Дата закрытия']):
                                                purchase_date = pd.to_datetime(purchase['Дата закрытия'], errors='coerce')
                                                if pd.notna(purchase_date) and purchase_date > lead_date:
                                                    purchased_count += 1
                                                    found_purchase = True
                                                    processed_contacts.add(contact_key)  # Отмечаем контакт как обработанный
                                                    break
                                    
                                    # 4. Если не нашли по _ym_uid, ищем по основному контакту
                                    if not found_purchase and pd.notna(lead['Основной контакт']) and lead['Основной контакт'] != '':
                                        successful_purchases = purchases_df[
                                            (purchases_df['Основной контакт'] == lead['Основной контакт']) & 
                                            (purchases_df['Этап сделки'] == 'Успешно реализовано')
                                        ]
                                        
                                        for _, purchase in successful_purchases.iterrows():
                                            if pd.notna(purchase['Дата закрытия']):
                                                purchase_date = pd.to_datetime(purchase['Дата закрытия'], errors='coerce')
                                                if pd.notna(purchase_date) and purchase_date > lead_date:
                                                    purchased_count += 1
                                                    found_purchase = True
                                                    processed_contacts.add(contact_key)  # Отмечаем контакт как обработанный
                                                    break
                                
                                purchased_results.append({
                                    'Месяц': month,
                                    'Источник трафика': source,
                                    'Купили': purchased_count
                                })
                            
                            # Создаем DataFrame с результатами покупок
                            purchased_df = pd.DataFrame(purchased_results)
                            
                            # Добавляем столбец "Купили" в аналитическую таблицу
                            analytics_df = analytics_df.merge(
                                purchased_df,
                                on=['Месяц', 'Источник трафика'],
                                how='left'
                            )
                            analytics_df['Купили'] = analytics_df['Купили'].fillna(0).astype(int)
                            
                                                        # Добавляем столбец "Конверсия в покупку (%)" - отношение купивших к предквалифицированным
                            analytics_df['Конверсия в покупку (%)'] = (
                                (analytics_df['Купили'] / analytics_df['Предквалифицированные лиды'] * 100)
                                .round(2)
                            ).fillna(0)
                            
                            # Добавляем столбец "Конверсия в активации (%)" - отношение новых активаций к купившим
                            analytics_df['Конверсия в активации (%)'] = (
                                (analytics_df['Новые активации ТСД'] / analytics_df['Купили'] * 100)
                                .round(2)
                            ).fillna(0)
                            
                            total_purchased = purchased_df['Купили'].sum()
                            st.success(f"✅ Анализ покупок завершен! Найдено {total_purchased} покупок среди предквалифицированных лидов")
                            
                        else:
                            st.warning("⚠️ Предквалифицированные лиды не найдены")
                            # Добавляем пустые столбцы
                            analytics_df['Купили'] = 0
                            analytics_df['Конверсия в покупку (%)'] = 0.0
                        
                        # Добавляем строку "Итого" в конец таблицы
                        # Создаем итоговые строки по каждому источнику трафика
                        total_rows = []
                        

                        
                        # Создаем новую таблицу с правильным порядком строк
                        ordered_rows = []
                        
                        # Проходим по каждому месяцу
                        for month in sorted(analytics_df['Месяц'].unique()):
                            # Добавляем все источники трафика для этого месяца
                            month_data = analytics_df[analytics_df['Месяц'] == month].sort_values('Источник трафика')
                            for _, row in month_data.iterrows():
                                ordered_rows.append(row.to_dict())
                            
                            # Добавляем итог по месяцу сразу после всех источников
                            month_summary = {
                                'Месяц': month,
                                'Источник трафика': 'ИТОГО ПО МЕСЯЦУ',
                                'Количество лидов': month_data['Количество лидов'].sum(),
                                'Предквалифицированные лиды': month_data['Предквалифицированные лиды'].sum(),
                                'Купили': month_data['Купили'].sum(),
                                'Конверсия в предквалификацию (%)': round(
                                    (month_data['Предквалифицированные лиды'].sum() / month_data['Количество лидов'].sum() * 100), 2
                                ) if month_data['Количество лидов'].sum() > 0 else 0,
                                'Конверсия в покупку (%)': round(
                                    (month_data['Купили'].sum() / month_data['Предквалифицированные лиды'].sum() * 100), 2
                                ) if month_data['Предквалифицированные лиды'].sum() > 0 else 0,
                                'Новые активации ТСД': month_data['Новые активации ТСД'].sum() if 'Новые активации ТСД' in month_data.columns else 0,
                                'Конверсия в активации (%)': round(
                                    (month_data['Новые активации ТСД'].sum() / month_data['Купили'].sum() * 100), 2
                                ) if month_data['Купили'].sum() > 0 else 0
                            }
                            ordered_rows.append(month_summary)
                        
                        # Добавляем итоги по каждому источнику трафика
                        for source in sorted(analytics_df['Источник трафика'].unique()):
                            source_data = analytics_df[analytics_df['Источник трафика'] == source]
                            source_summary = {
                                'Месяц': 'Итого',
                                'Источник трафика': source,
                                'Количество лидов': source_data['Количество лидов'].sum(),
                                'Предквалифицированные лиды': source_data['Предквалифицированные лиды'].sum(),
                                'Купили': source_data['Купили'].sum(),
                                'Конверсия в предквалификацию (%)': round(
                                    (source_data['Предквалифицированные лиды'].sum() / source_data['Количество лидов'].sum() * 100), 2
                                ) if source_data['Количество лидов'].sum() > 0 else 0,
                                'Конверсия в покупку (%)': round(
                                    (source_data['Купили'].sum() / source_data['Предквалифицированные лиды'].sum() * 100), 2
                                ) if source_data['Предквалифицированные лиды'].sum() > 0 else 0,
                                'Новые активации ТСД': source_data['Новые активации ТСД'].sum() if 'Новые активации ТСД' in source_data.columns else 0,
                                'Конверсия в активации (%)': round(
                                    (source_data['Новые активации ТСД'].sum() / source_data['Купили'].sum() * 100), 2
                                ) if source_data['Купили'].sum() > 0 else 0
                            }
                            ordered_rows.append(source_summary)
                        
                        # Добавляем общую итоговую строку
                        overall_summary = {
                            'Месяц': 'Итого',
                            'Источник трафика': 'ВСЕ ИСТОЧНИКИ',
                            'Количество лидов': analytics_df['Количество лидов'].sum(),
                            'Предквалифицированные лиды': analytics_df['Предквалифицированные лиды'].sum(),
                            'Купили': analytics_df['Купили'].sum(),
                            'Конверсия в покупку (%)': round(
                                (analytics_df['Купили'].sum() / analytics_df['Предквалифицированные лиды'].sum() * 100), 2
                            ) if analytics_df['Предквалифицированные лиды'].sum() > 0 else 0,
                            'Новые активации ТСД': analytics_df['Новые активации ТСД'].sum() if 'Новые активации ТСД' in analytics_df.columns else 0,
                            'Конверсия в активации (%)': round(
                                (analytics_df['Новые активации ТСД'].sum() / analytics_df['Купили'].sum() * 100), 2
                            ) if analytics_df['Купили'].sum() > 0 else 0
                        }
                        ordered_rows.append(overall_summary)
                        
                        # Создаем итоговую таблицу с правильным порядком
                        analytics_df_with_total = pd.DataFrame(ordered_rows)
                        

                        
                        # Рассчитываем общие метрики для панели
                        total_leads = analytics_df['Количество лидов'].sum()
                        total_prequalified = analytics_df['Предквалифицированные лиды'].sum()
                        total_purchased = analytics_df['Купили'].sum()
                        
                        # БЕЗОПАСНО получаем сумму новых активаций
                        total_new_activations = analytics_df['Новые активации ТСД'].sum()
                        
                        # Средние конверсии
                        avg_lead_to_sql = round((total_prequalified / total_leads * 100), 2) if total_leads > 0 else 0
                        avg_sql_to_sale = round((total_purchased / total_prequalified * 100), 2) if total_prequalified > 0 else 0
                        
                        # Отображаем панель с метриками
                        st.subheader("📊 КЛЮЧЕВЫЕ ПОКАЗАТЕЛИ")
                        
                        # Создаем 6 колонок для метрик
                        col1, col2, col3, col4, col5, col6 = st.columns(6)
                        
                        with col1:
                            st.metric(
                                label="Лиды",
                                value=f"{total_leads:,}".replace(",", " "),
                                help="Общее количество лидов"
                            )
                        
                        with col2:
                            st.metric(
                                label="SQL",
                                value=f"{total_prequalified:,}".replace(",", " "),
                                help="Количество предквалифицированных лидов"
                            )
                        
                        with col3:
                            st.metric(
                                label="Купили",
                                value=f"{total_purchased:,}".replace(",", " "),
                                help="Количество успешных продаж"
                            )
                        
                        with col4:
                            # БЕЗОПАСНО отображаем метрику новых активаций
                            try:
                                st.metric(
                                    label="Новые активации ТСД",
                                    value=f"{total_new_activations:,}".replace(",", " "),
                                    help="Количество новых активаций ТСД"
                                )
                            except:
                                st.metric(
                                    label="Новые активации ТСД",
                                    value="0",
                                    help="Количество новых активаций ТСД"
                                )
                        
                        with col5:
                            st.metric(
                                label="Конверсия Лид → SQL",
                                value=f"{avg_lead_to_sql}%",
                                help="Средняя конверсия лидов в предквалифицированные"
                            )
                        
                        with col6:
                            st.metric(
                                label="Конверсия SQL → Продажа",
                                value=f"{avg_sql_to_sale}%",
                                help="Средняя конверсия предквалифицированных в продажи"
                            )
                        
                        # Добавляем разделитель
                        st.markdown("---")
                        
                        # Конвертируем Period в строку для отображения
                        analytics_df_with_total['Месяц'] = analytics_df_with_total['Месяц'].astype(str)
                        
                        # Создаем визуальный эффект объединенных ячеек для месяцев
                        # Месяц отображается только в первой строке каждого месяца
                        month_display = analytics_df_with_total['Месяц'].copy()
                        current_month = None
                        
                        for idx in range(len(analytics_df_with_total)):
                            month = analytics_df_with_total.iloc[idx]['Месяц']
                            source = analytics_df_with_total.iloc[idx]['Источник трафика']
                            
                            # Для строк "ИТОГО ПО МЕСЯЦУ" оставляем месяц как есть
                            if source == 'ИТОГО ПО МЕСЯЦУ':
                                month_display.iloc[idx] = month
                                current_month = month
                            elif month != current_month:
                                current_month = month
                                # Оставляем месяц как есть для первой строки
                            else:
                                # Для остальных строк того же месяца делаем пустую строку
                                month_display.iloc[idx] = ''
                        
                        # Создаем копию для отображения с модифицированным столбцом месяца
                        display_df = analytics_df_with_total.copy()
                        display_df['Месяц'] = month_display
                        
                        # Переупорядочиваем столбцы - "Новые активации ТСД" предпоследний, "Конверсия в активации (%)" последний
                        if 'Новые активации ТСД' in display_df.columns and 'Конверсия в активации (%)' in display_df.columns:
                            # Получаем все столбцы кроме "Новые активации ТСД" и "Конверсия в активации (%)"
                            other_columns = [col for col in display_df.columns if col not in ['Новые активации ТСД', 'Конверсия в активации (%)']]
                            # Создаем новый порядок столбцов: другие столбцы + "Новые активации ТСД" + "Конверсия в активации (%)"
                            new_column_order = other_columns + ['Новые активации ТСД', 'Конверсия в активации (%)']
                            # Переупорядочиваем DataFrame
                            display_df = display_df[new_column_order]
                            st.info("✅ Столбцы переупорядочены: 'Новые активации ТСД' предпоследний, 'Конверсия в активации (%)' последний")
                        
                        st.success(f"✅ Аналитическая таблица создана! Размер: {analytics_df.shape[0]} строк, {analytics_df.shape[1]} столбцов")
                        st.info(f"📊 Анализ основан на всех {len(leads_analysis_clean)} лидах из leads2025")
                        
                        # Показываем аналитическую таблицу с итогами
                        st.subheader("📈 Аналитика лидов по месяцам:")
                        
                        # Проверяем наличие столбца "Новые активации ТСД"
                        if 'Новые активации ТСД' in display_df.columns:
                            st.success("✅ Столбец 'Новые активации ТСД' добавлен в таблицу")
                        else:
                            st.warning("⚠️ Столбец 'Новые активации ТСД' отсутствует в таблице")
                        
                        # Показываем одну таблицу с сегментацией по дате и источнику трафика
                        st.dataframe(display_df, use_container_width=True)
                        
                        # График по источникам трафика (теперь встроен в основную таблицу)
                        st.subheader("📈 График лидов по источникам трафика:")
                        
                        # Создаем график на основе основной таблицы
                        fig_traffic = go.Figure()
                        
                        # Добавляем линии для каждого источника трафика
                        for source in analytics_df['Источник трафика'].unique():
                            source_data = analytics_df[analytics_df['Источник трафика'] == source]
                            source_data['Месяц'] = source_data['Месяц'].astype(str)
                            
                            fig_traffic.add_trace(
                                go.Scatter(
                                    x=source_data['Месяц'],
                                    y=source_data['Количество лидов'],
                                    mode='lines+markers',
                                    name=source,
                                    line=dict(width=3)
                                )
                            )
                        
                        fig_traffic.update_layout(
                            height=500,
                            title_text="Динамика лидов по источникам трафика",
                            xaxis_title="Месяц",
                            yaxis_title="Количество лидов",
                            showlegend=True
                        )
                        
                        st.plotly_chart(fig_traffic, use_container_width=True)
                        
                        # Создаем график
                        st.subheader("📊 График динамики лидов по месяцам:")
                        
                        # Конвертируем Period в строку для отображения
                        analytics_df_display = analytics_df.reset_index()
                        analytics_df_display['Месяц'] = analytics_df_display['Месяц'].astype(str)
                        
                        # Создаем график с двумя линиями
                        import plotly.express as px
                        import plotly.graph_objects as go
                        from plotly.subplots import make_subplots
                        
                        fig = make_subplots(
                            rows=2, cols=1,
                            subplot_titles=('Количество лидов по месяцам', 'Конверсия в предквалификацию (%)'),
                            vertical_spacing=0.1
                        )
                        
                        # Первый график - количество лидов
                        fig.add_trace(
                            go.Scatter(
                                x=analytics_df_display['Месяц'],
                                y=analytics_df_display['Количество лидов'],
                                mode='lines+markers',
                                name='Количество лидов',
                                line=dict(color='blue', width=3)
                            ),
                            row=1, col=1
                        )
                        
                        fig.add_trace(
                            go.Scatter(
                                x=analytics_df_display['Месяц'],
                                y=analytics_df_display['Предквалифицированные лиды'],
                                mode='lines+markers',
                                name='Предквалифицированные лиды',
                                line=dict(color='green', width=3)
                            ),
                            row=1, col=1
                        )
                        
                        # Второй график - конверсия
                        fig.add_trace(
                            go.Scatter(
                                x=analytics_df_display['Месяц'],
                                y=analytics_df_display['Конверсия в предквалификацию (%)'],
                                mode='lines+markers',
                                name='Конверсия (%)',
                                line=dict(color='red', width=3)
                            ),
                            row=2, col=1
                        )
                        
                        fig.update_layout(
                            height=600,
                            title_text="Динамика лидов и конверсии по месяцам",
                            showlegend=True
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # ===== ТАБЛИЦА 2: Аналитика лидов по месяцам (без сегментации по источникам) =====
                        st.subheader("📊 ТАБЛИЦА 2: Аналитика лидов по месяцам (без сегментации по источникам)")
                        
                        try:
                            st.info("📋 Создаем аналитическую таблицу 2 без сегментации по источникам...")
                            
                            # Создаем аналитическую таблицу только по месяцам
                            analytics_df_monthly = leads_analysis_clean.groupby(['Месяц']).agg({
                                'ID': 'count',  # Количество лидов по месяцам
                            }).rename(columns={
                                'ID': 'Количество лидов'
                            }).reset_index()
                            
                            # Добавляем столбец "Новые активации ТСД" и инициализируем нулями
                            analytics_df_monthly['Новые активации ТСД'] = 0
                            
                            # Если есть данные об активациях, заполняем столбец
                            if 'total_new_activations' in locals() and total_new_activations > 0:
                                # Распределяем активации по месяцам пропорционально количеству лидов
                                total_leads_monthly = analytics_df_monthly['Количество лидов'].sum()
                                for idx, row in analytics_df_monthly.iterrows():
                                    month = row['Месяц']
                                    month_leads = row['Количество лидов']
                                    # Пропорционально распределяем активации
                                    month_activations = int((month_leads / total_leads_monthly) * total_new_activations)
                                    analytics_df_monthly.loc[idx, 'Новые активации ТСД'] = month_activations
                            
                            # Создаем маску для предквалифицированных лидов
                            prequalified_mask_monthly = leads_analysis_clean['Этап сделки'] == 'Лид предквалифицирован'
                            
                            # Группируем предквалифицированные лиды только по месяцам
                            prequalified_by_month = leads_analysis_clean[prequalified_mask_monthly].groupby(['Месяц'])['ID'].count().reset_index()
                            prequalified_by_month = prequalified_by_month.rename(columns={'ID': 'Предквалифицированные лиды'})
                            
                            # Объединяем основную таблицу с предквалифицированными лидами
                            analytics_df_monthly = analytics_df_monthly.merge(
                                prequalified_by_month,
                                on=['Месяц'],
                                how='left'
                            )
                            
                            # Заполняем NaN значения нулями
                            analytics_df_monthly['Предквалифицированные лиды'] = analytics_df_monthly['Предквалифицированные лиды'].fillna(0).astype(int)
                            
                            # Добавляем столбец конверсии в предквалификацию
                            analytics_df_monthly['Конверсия в предквалификацию (%)'] = (
                                (analytics_df_monthly['Предквалифицированные лиды'] / analytics_df_monthly['Количество лидов'] * 100)
                                .round(2)
                            )
                            
                            # Сортируем по месяцам
                            analytics_df_monthly = analytics_df_monthly.sort_values('Месяц')
                            
                            # Анализируем покупки среди предквалифицированных лидов (только по месяцам)
                            st.info("🔍 Анализируем покупки среди предквалифицированных лидов (по месяцам)...")
                            
                            if len(prequalified_leads) > 0:
                                # Создаем DataFrame для хранения результатов покупок по месяцам
                                purchased_results_monthly = []
                                
                                # Создаем множество для отслеживания уже учтенных контактов
                                processed_contacts_monthly = set()
                                
                                # Анализируем каждый месяц отдельно
                                for month in sorted(leads_analysis_clean['Месяц'].unique()):
                                    month_leads = prequalified_leads[prequalified_leads['Месяц'] == month]
                                    purchased_count = 0
                                    
                                    # Для каждого лида в месяце ищем покупки
                                    for _, lead in month_leads.iterrows():
                                        found_purchase = False
                                        
                                        # Создаем уникальный идентификатор контакта для проверки дубликатов
                                        contact_key = None
                                        
                                        # Определяем ключ контакта (приоритет: ClientID > Yclid > _ym_uid > Основной контакт)
                                        if pd.notna(lead['ClientID']) and lead['ClientID'] != '':
                                            contact_key = f"ClientID_{lead['ClientID']}"
                                        elif pd.notna(lead['Yclid']) and lead['Yclid'] != '':
                                            contact_key = f"Yclid_{lead['Yclid']}"
                                        elif pd.notna(lead['_ym_uid']) and lead['_ym_uid'] != '':
                                            contact_key = f"_ym_uid_{lead['_ym_uid']}"
                                        elif pd.notna(lead['Основной контакт']) and lead['Основной контакт'] != '':
                                            contact_key = f"Contact_{lead['Основной контакт']}"
                                        
                                        # Проверяем, не обрабатывали ли мы уже этот контакт
                                        if contact_key is None or contact_key in processed_contacts_monthly:
                                            continue
                                        
                                        # Получаем дату создания лида
                                        lead_date = lead['Дата создания']
                                        
                                        # Ищем покупки по всем идентификаторам
                                        for identifier_col in ['ClientID', 'Yclid', '_ym_uid', 'Основной контакт']:
                                            if not found_purchase and pd.notna(lead[identifier_col]) and lead[identifier_col] != '':
                                                successful_purchases = purchases_df[
                                                    (purchases_df[identifier_col] == lead[identifier_col]) & 
                                                    (purchases_df['Этап сделки'] == 'Успешно реализовано')
                                                ]
                                                
                                                for _, purchase in successful_purchases.iterrows():
                                                    if pd.notna(purchase['Дата закрытия']):
                                                        purchase_date = pd.to_datetime(purchase['Дата закрытия'], errors='coerce')
                                                        if pd.notna(purchase_date) and purchase_date > lead_date:
                                                            purchased_count += 1
                                                            found_purchase = True
                                                            processed_contacts_monthly.add(contact_key)
                                                            break
                                                
                                                if found_purchase:
                                                    break
                                        
                                        if found_purchase:
                                            break
                                    
                                    purchased_results_monthly.append({
                                        'Месяц': month,
                                        'Купили': purchased_count
                                    })
                                
                                # Создаем DataFrame с результатами покупок
                                purchased_df_monthly = pd.DataFrame(purchased_results_monthly)
                                
                                # Добавляем столбец "Купили" в аналитическую таблицу
                                analytics_df_monthly = analytics_df_monthly.merge(
                                    purchased_df_monthly,
                                    on=['Месяц'],
                                    how='left'
                                )
                                analytics_df_monthly['Купили'] = analytics_df_monthly['Купили'].fillna(0).astype(int)
                                
                                # Добавляем столбец "Конверсия в покупку (%)"
                                analytics_df_monthly['Конверсия в покупку (%)'] = (
                                    (analytics_df_monthly['Купили'] / analytics_df_monthly['Предквалифицированные лиды'] * 100)
                                    .round(2)
                                ).fillna(0)
                                
                                # Добавляем столбец "Конверсия в активации (%)"
                                analytics_df_monthly['Конверсия в активации (%)'] = (
                                    (analytics_df_monthly['Новые активации ТСД'] / analytics_df_monthly['Купили'] * 100)
                                    .round(2)
                                ).fillna(0)
                                
                                total_purchased_monthly = purchased_df_monthly['Купили'].sum()
                                st.success(f"✅ Анализ покупок по месяцам завершен! Найдено {total_purchased_monthly} покупок")
                                
                            else:
                                st.warning("⚠️ Предквалифицированные лиды не найдены")
                                # Добавляем пустые столбцы
                                analytics_df_monthly['Купили'] = 0
                                analytics_df_monthly['Конверсия в покупку (%)'] = 0.0
                                analytics_df_monthly['Конверсия в активации (%)'] = 0.0
                            
                            # Добавляем итоговую строку
                            total_monthly = {
                                'Месяц': 'Итого',
                                'Количество лидов': analytics_df_monthly['Количество лидов'].sum(),
                                'Предквалифицированные лиды': analytics_df_monthly['Предквалифицированные лиды'].sum(),
                                'Купили': analytics_df_monthly['Купили'].sum(),
                                'Конверсия в предквалификацию (%)': round(
                                    (analytics_df_monthly['Предквалифицированные лиды'].sum() / analytics_df_monthly['Количество лидов'].sum() * 100), 2
                                ) if analytics_df_monthly['Количество лидов'].sum() > 0 else 0,
                                'Конверсия в покупку (%)': round(
                                    (analytics_df_monthly['Купили'].sum() / analytics_df_monthly['Предквалифицированные лиды'].sum() * 100), 2
                                ) if analytics_df_monthly['Предквалифицированные лиды'].sum() > 0 else 0,
                                'Новые активации ТСД': analytics_df_monthly['Новые активации ТСД'].sum(),
                                'Конверсия в активации (%)': round(
                                    (analytics_df_monthly['Новые активации ТСД'].sum() / analytics_df_monthly['Купили'].sum() * 100), 2
                                ) if analytics_df_monthly['Купили'].sum() > 0 else 0
                            }
                            
                            # Создаем итоговую таблицу с итоговой строкой
                            analytics_df_monthly_with_total = pd.concat([
                                analytics_df_monthly,
                                pd.DataFrame([total_monthly])
                            ], ignore_index=True)
                            
                            # Конвертируем Period в строку для отображения
                            analytics_df_monthly_with_total['Месяц'] = analytics_df_monthly_with_total['Месяц'].astype(str)
                            
                            # Переупорядочиваем столбцы - "Новые активации ТСД" предпоследний, "Конверсия в активации (%)" последний
                            if 'Новые активации ТСД' in analytics_df_monthly_with_total.columns and 'Конверсия в активации (%)' in analytics_df_monthly_with_total.columns:
                                other_columns = [col for col in analytics_df_monthly_with_total.columns if col not in ['Новые активации ТСД', 'Конверсия в активации (%)']]
                                new_column_order = other_columns + ['Новые активации ТСД', 'Конверсия в активации (%)']
                                analytics_df_monthly_with_total = analytics_df_monthly_with_total[new_column_order]
                                st.info("✅ Столбцы переупорядочены: 'Новые активации ТСД' предпоследний, 'Конверсия в активации (%)' последний")
                            
                            st.success(f"✅ Аналитическая таблица 2 создана! Размер: {len(analytics_df_monthly)} строк, {len(analytics_df_monthly.columns)} столбцов")
                            
                            # Показываем аналитическую таблицу 2
                            st.dataframe(analytics_df_monthly_with_total, use_container_width=True)
                            
                            # Создаем график для таблицы 2
                            st.subheader("📈 График динамики лидов по месяцам (без сегментации по источникам):")
                            
                            # Конвертируем Period в строку для отображения
                            analytics_df_monthly_display = analytics_df_monthly.reset_index()
                            analytics_df_monthly_display['Месяц'] = analytics_df_monthly_display['Месяц'].astype(str)
                            
                            # Создаем график с двумя линиями
                            fig_monthly = make_subplots(
                                rows=2, cols=1,
                                subplot_titles=('Количество лидов по месяцам', 'Конверсия в предквалификацию (%)'),
                                vertical_spacing=0.1
                            )
                            
                            # Первый график - количество лидов
                            fig_monthly.add_trace(
                                go.Scatter(
                                    x=analytics_df_monthly_display['Месяц'],
                                    y=analytics_df_monthly_display['Количество лидов'],
                                    mode='lines+markers',
                                    name='Количество лидов',
                                    line=dict(color='blue', width=3)
                                ),
                                row=1, col=1
                            )
                            
                            fig_monthly.add_trace(
                                go.Scatter(
                                    x=analytics_df_monthly_display['Месяц'],
                                    y=analytics_df_monthly_display['Предквалифицированные лиды'],
                                    mode='lines+markers',
                                    name='Предквалифицированные лиды',
                                    line=dict(color='green', width=3)
                                ),
                                row=1, col=1
                            )
                            
                            # Второй график - конверсия
                            fig_monthly.add_trace(
                                go.Scatter(
                                    x=analytics_df_monthly_display['Месяц'],
                                    y=analytics_df_monthly_display['Конверсия в предквалификацию (%)'],
                                    mode='lines+markers',
                                    name='Конверсия (%)',
                                    line=dict(color='red', width=3)
                                ),
                                row=2, col=1
                            )
                            
                            fig_monthly.update_layout(
                                height=600,
                                title_text="Динамика лидов и конверсии по месяцам (без сегментации по источникам)",
                                showlegend=True
                            )
                            
                            st.plotly_chart(fig_monthly, use_container_width=True)
                            
                        except Exception as e:
                            st.error(f"❌ Ошибка при создании аналитической таблицы 2: {str(e)}")
                        
                        # ===== КОНЕЦ ТАБЛИЦЫ 2 =====
                        
                    else:
                        st.error("❌ Столбец 'Этап сделки' не найден в данных")
                        
                else:
                    st.warning("⚠️ Нет данных с корректными датами для анализа")
                    
            else:
                st.error("❌ Столбец 'Дата создания' не найден в данных")
                
        except Exception as e:
            st.error(f"❌ Ошибка при создании аналитической таблицы: {str(e)}")
            analytics_df = None
            
    else:
        st.warning("⚠️ Некоторые файлы не удалось загрузить. Проверьте наличие файлов в директории.")
    
    # ===== ТАБЛИЦА 2: Аналитика лидов по месяцам (без сегментации по источникам) =====
    # Эта таблица отображается всегда, независимо от условий основной таблицы
    st.subheader("📊 ТАБЛИЦА 2: Аналитика лидов по месяцам (без сегментации по источникам)")
    
    try:
        st.info("📋 Создаем аналитическую таблицу 2 без сегментации по источникам...")
        
        # Проверяем, есть ли данные для анализа
        if 'leads_df' in locals() and len(leads_df) > 0:
            # Создаем аналитическую таблицу только по месяцам
            leads_monthly = leads_df.copy()
            
            # Обрабатываем столбец 'Дата создания'
            if 'Дата создания' in leads_monthly.columns:
                leads_monthly['Дата создания'] = pd.to_datetime(leads_monthly['Дата создания'], errors='coerce')
                leads_monthly['Месяц'] = leads_monthly['Дата создания'].dt.to_period('M')
                leads_monthly_clean = leads_monthly[leads_monthly['Месяц'].notna()].copy()
                
                if len(leads_monthly_clean) > 0:
                    # Создаем аналитическую таблицу только по месяцам
                    analytics_df_monthly = leads_monthly_clean.groupby(['Месяц']).agg({
                        'ID': 'count',  # Количество лидов по месяцам
                    }).rename(columns={
                        'ID': 'Количество лидов'
                    }).reset_index()
                    
                    # Добавляем столбец "Новые активации ТСД" и инициализируем нулями
                    analytics_df_monthly['Новые активации ТСД'] = 0
                    
                    # Если есть данные об активациях, заполняем столбец
                    if 'total_new_activations' in locals() and total_new_activations > 0:
                        # Распределяем активации по месяцам пропорционально количеству лидов
                        total_leads_monthly = analytics_df_monthly['Количество лидов'].sum()
                        for idx, row in analytics_df_monthly.iterrows():
                            month = row['Месяц']
                            month_leads = row['Количество лидов']
                            # Пропорционально распределяем активации
                            month_activations = int((month_leads / total_leads_monthly) * total_new_activations)
                            analytics_df_monthly.loc[idx, 'Новые активации ТСД'] = month_activations
                    
                    # Создаем маску для предквалифицированных лидов
                    if 'Этап сделки' in leads_monthly_clean.columns:
                        prequalified_mask_monthly = leads_monthly_clean['Этап сделки'] == 'Лид предквалифицирован'
                        
                        # Группируем предквалифицированные лиды только по месяцам
                        prequalified_by_month = leads_monthly_clean[prequalified_mask_monthly].groupby(['Месяц'])['ID'].count().reset_index()
                        prequalified_by_month = prequalified_by_month.rename(columns={'ID': 'Предквалифицированные лиды'})
                        
                        # Объединяем основную таблицу с предквалифицированными лидами
                        analytics_df_monthly = analytics_df_monthly.merge(
                            prequalified_by_month,
                            on=['Месяц'],
                            how='left'
                        )
                        
                        # Заполняем NaN значения нулями
                        analytics_df_monthly['Предквалифицированные лиды'] = analytics_df_monthly['Предквалифицированные лиды'].fillna(0).astype(int)
                        
                        # Добавляем столбец конверсии в предквалификацию
                        analytics_df_monthly['Конверсия в предквалификацию (%)'] = (
                            (analytics_df_monthly['Предквалифицированные лиды'] / analytics_df_monthly['Количество лидов'] * 100)
                            .round(2)
                        )
                        
                        # Сортируем по месяцам
                        analytics_df_monthly = analytics_df_monthly.sort_values('Месяц')
                        
                        # Анализируем покупки среди предквалифицированных лидов (только по месяцам)
                        st.info("🔍 Анализируем покупки среди предквалифицированных лидов (по месяцам)...")
                        
                        prequalified_leads_monthly = leads_monthly_clean[prequalified_mask_monthly].copy()
                        
                        if len(prequalified_leads_monthly) > 0:
                            # Создаем DataFrame для хранения результатов покупок по месяцам
                            purchased_results_monthly = []
                            
                            # Создаем множество для отслеживания уже учтенных контактов
                            processed_contacts_monthly = set()
                            
                            # Анализируем каждый месяц отдельно
                            for month in sorted(leads_monthly_clean['Месяц'].unique()):
                                month_leads = prequalified_leads_monthly[prequalified_leads_monthly['Месяц'] == month]
                                purchased_count = 0
                                
                                # Для каждого лида в месяце ищем покупки
                                for _, lead in month_leads.iterrows():
                                    found_purchase = False
                                    
                                    # Создаем уникальный идентификатор контакта для проверки дубликатов
                                    contact_key = None
                                    
                                    # Определяем ключ контакта (приоритет: ClientID > Yclid > _ym_uid > Основной контакт)
                                    if pd.notna(lead['ClientID']) and lead['ClientID'] != '':
                                        contact_key = f"ClientID_{lead['ClientID']}"
                                    elif pd.notna(lead['Yclid']) and lead['Yclid'] != '':
                                        contact_key = f"Yclid_{lead['Yclid']}"
                                    elif pd.notna(lead['_ym_uid']) and lead['_ym_uid'] != '':
                                        contact_key = f"_ym_uid_{lead['_ym_uid']}"
                                    elif pd.notna(lead['Основной контакт']) and lead['Основной контакт'] != '':
                                        contact_key = f"Contact_{lead['Основной контакт']}"
                                    
                                    # Проверяем, не обрабатывали ли мы уже этот контакт
                                    if contact_key is None or contact_key in processed_contacts_monthly:
                                        continue
                                    
                                    # Получаем дату создания лида
                                    lead_date = lead['Дата создания']
                                    
                                    # Ищем покупки по всем идентификаторам
                                    if 'purchases_df' in locals() and len(purchases_df) > 0:
                                        for identifier_col in ['ClientID', 'Yclid', '_ym_uid', 'Основной контакт']:
                                            if not found_purchase and pd.notna(lead[identifier_col]) and lead[identifier_col] != '':
                                                if identifier_col in purchases_df.columns and 'Этап сделки' in purchases_df.columns:
                                                    successful_purchases = purchases_df[
                                                        (purchases_df[identifier_col] == lead[identifier_col]) & 
                                                        (purchases_df['Этап сделки'] == 'Успешно реализовано')
                                                    ]
                                                    
                                                    for _, purchase in successful_purchases.iterrows():
                                                        if pd.notna(purchase['Дата закрытия']):
                                                            purchase_date = pd.to_datetime(purchase['Дата закрытия'], errors='coerce')
                                                            if pd.notna(purchase_date) and purchase_date > lead_date:
                                                                purchased_count += 1
                                                                found_purchase = True
                                                                processed_contacts_monthly.add(contact_key)
                                                                break
                                                
                                                if found_purchase:
                                                    break
                                        
                                        if found_purchase:
                                            break
                                
                                purchased_results_monthly.append({
                                    'Месяц': month,
                                    'Купили': purchased_count
                                })
                            
                            # Создаем DataFrame с результатами покупок
                            purchased_df_monthly = pd.DataFrame(purchased_results_monthly)
                            
                            # Добавляем столбец "Купили" в аналитическую таблицу
                            analytics_df_monthly = analytics_df_monthly.merge(
                                purchased_df_monthly,
                                on=['Месяц'],
                                how='left'
                            )
                            analytics_df_monthly['Купили'] = analytics_df_monthly['Купили'].fillna(0).astype(int)
                            
                            # Добавляем столбец "Конверсия в покупку (%)"
                            analytics_df_monthly['Конверсия в покупку (%)'] = (
                                (analytics_df_monthly['Купили'] / analytics_df_monthly['Предквалифицированные лиды'] * 100)
                                .round(2)
                            ).fillna(0)
                            
                            # Добавляем столбец "Конверсия в активации (%)"
                            analytics_df_monthly['Конверсия в активации (%)'] = (
                                (analytics_df_monthly['Новые активации ТСД'] / analytics_df_monthly['Купили'] * 100)
                                .round(2)
                            ).fillna(0)
                            
                            total_purchased_monthly = purchased_df_monthly['Купили'].sum()
                            st.success(f"✅ Анализ покупок по месяцам завершен! Найдено {total_purchased_monthly} покупок")
                            
                        else:
                            st.warning("⚠️ Предквалифицированные лиды не найдены")
                            # Добавляем пустые столбцы
                            analytics_df_monthly['Купили'] = 0
                            analytics_df_monthly['Конверсия в покупку (%)'] = 0.0
                            analytics_df_monthly['Конверсия в активации (%)'] = 0.0
                        
                        # Добавляем итоговую строку
                        total_monthly = {
                            'Месяц': 'Итого',
                            'Количество лидов': analytics_df_monthly['Количество лидов'].sum(),
                            'Предквалифицированные лиды': analytics_df_monthly['Предквалифицированные лиды'].sum(),
                            'Купили': analytics_df_monthly['Купили'].sum(),
                            'Конверсия в предквалификацию (%)': round(
                                (analytics_df_monthly['Предквалифицированные лиды'].sum() / analytics_df_monthly['Количество лидов'].sum() * 100), 2
                            ) if analytics_df_monthly['Количество лидов'].sum() > 0 else 0,
                            'Конверсия в покупку (%)': round(
                                (analytics_df_monthly['Купили'].sum() / analytics_df_monthly['Предквалифицированные лиды'].sum() * 100), 2
                            ) if analytics_df_monthly['Предквалифицированные лиды'].sum() > 0 else 0,
                            'Новые активации ТСД': analytics_df_monthly['Новые активации ТСД'].sum(),
                            'Конверсия в активации (%)': round(
                                (analytics_df_monthly['Новые активации ТСД'].sum() / analytics_df_monthly['Купили'].sum() * 100), 2
                            ) if analytics_df_monthly['Купили'].sum() > 0 else 0
                        }
                        
                        # Создаем итоговую таблицу с итоговой строкой
                        analytics_df_monthly_with_total = pd.concat([
                            analytics_df_monthly,
                            pd.DataFrame([total_monthly])
                        ], ignore_index=True)
                        
                        # Конвертируем Period в строку для отображения
                        analytics_df_monthly_with_total['Месяц'] = analytics_df_monthly_with_total['Месяц'].astype(str)
                        
                        # Переупорядочиваем столбцы - "Новые активации ТСД" предпоследний, "Конверсия в активации (%)" последний
                        if 'Новые активации ТСД' in analytics_df_monthly_with_total.columns and 'Конверсия в активации (%)' in analytics_df_monthly_with_total.columns:
                            other_columns = [col for col in analytics_df_monthly_with_total.columns if col not in ['Новые активации ТСД', 'Конверсия в активации (%)']]
                            new_column_order = other_columns + ['Новые активации ТСД', 'Конверсия в активации (%)']
                            analytics_df_monthly_with_total = analytics_df_monthly_with_total[new_column_order]
                            st.info("✅ Столбцы переупорядочены: 'Новые активации ТСД' предпоследний, 'Конверсия в активации (%)' последний")
                        
                        st.success(f"✅ Аналитическая таблица 2 создана! Размер: {len(analytics_df_monthly)} строк, {len(analytics_df_monthly.columns)} столбцов")
                        
                        # Показываем аналитическую таблицу 2
                        st.dataframe(analytics_df_monthly_with_total, use_container_width=True)
                        
                        # Создаем график для таблицы 2
                        st.subheader("📈 График динамики лидов по месяцам (без сегментации по источникам):")
                        
                        # Конвертируем Period в строку для отображения
                        analytics_df_monthly_display = analytics_df_monthly.reset_index()
                        analytics_df_monthly_display['Месяц'] = analytics_df_monthly_display['Месяц'].astype(str)
                        
                        # Создаем график с двумя линиями
                        fig_monthly = make_subplots(
                            rows=2, cols=1,
                            subplot_titles=('Количество лидов по месяцам', 'Конверсия в предквалификацию (%)'),
                            vertical_spacing=0.1
                        )
                        
                        # Первый график - количество лидов
                        fig_monthly.add_trace(
                            go.Scatter(
                                x=analytics_df_monthly_display['Месяц'],
                                y=analytics_df_monthly_display['Количество лидов'],
                                mode='lines+markers',
                                name='Количество лидов',
                                line=dict(color='blue', width=3)
                            ),
                            row=1, col=1
                        )
                        
                        fig_monthly.add_trace(
                            go.Scatter(
                                x=analytics_df_monthly_display['Месяц'],
                                y=analytics_df_monthly_display['Предквалифицированные лиды'],
                                mode='lines+markers',
                                name='Предквалифицированные лиды',
                                line=dict(color='green', width=3)
                            ),
                            row=1, col=1
                        )
                        
                        # Второй график - конверсия
                        fig_monthly.add_trace(
                            go.Scatter(
                                x=analytics_df_monthly_display['Месяц'],
                                y=analytics_df_monthly_display['Конверсия в предквалификацию (%)'],
                                mode='lines+markers',
                                name='Конверсия (%)',
                                line=dict(color='red', width=3)
                            ),
                            row=2, col=1
                        )
                        
                        fig_monthly.update_layout(
                            height=600,
                            title_text="Динамика лидов и конверсии по месяцам (без сегментации по источникам)",
                            showlegend=True
                        )
                        
                        st.plotly_chart(fig_monthly, use_container_width=True)
                        
                    else:
                        st.warning("⚠️ Столбец 'Этап сделки' не найден в данных")
                        
                else:
                    st.warning("⚠️ Нет данных с корректными датами для анализа")
                    
            else:
                st.warning("⚠️ Столбец 'Дата создания' не найден в данных")
        else:
            st.warning("⚠️ Нет данных о лидах для создания таблицы 2")
            
    except Exception as e:
        st.error(f"❌ Ошибка при создании аналитической таблицы 2: {str(e)}")
    
    # ===== КОНЕЦ ТАБЛИЦЫ 2 =====

if __name__ == "__main__":
    main()