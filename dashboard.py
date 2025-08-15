import pandas as pd
import streamlit as st
import plotly.graph_objects as go

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

# Проверяем, что все файлы загружены успешно
if leads_df is not None and purchases_df is not None and ymetrica_df is not None:
    st.success("🎉 Все файлы успешно загружены!")
    
    # Показываем краткую информацию о данных
    st.subheader("📊 Краткая информация о данных:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Лиды", f"{leads_df.shape[0]:,}")
        st.metric("Столбцы лидов", leads_df.shape[1])
        
    with col2:
        st.metric("Покупки", f"{purchases_df.shape[0]:,}")
        st.metric("Столбцы покупок", purchases_df.shape[1])
        
    with col3:
        st.metric("События YM", f"{ymetrica_df.shape[0]:,}")
        st.metric("Столбцы YM", ymetrica_df.shape[1])
    
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
                            ) if month_data['Предквалифицированные лиды'].sum() > 0 else 0
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
                        'Конверсия в предквалификацию (%)': round(
                            (analytics_df['Предквалифицированные лиды'].sum() / analytics_df['Количество лидов'].sum() * 100), 2
                        ) if analytics_df['Количество лидов'].sum() > 0 else 0,
                        'Конверсия в покупку (%)': round(
                            (analytics_df['Купили'].sum() / analytics_df['Предквалифицированные лиды'].sum() * 100), 2
                        ) if analytics_df['Предквалифицированные лиды'].sum() > 0 else 0
                    }
                    ordered_rows.append(overall_summary)
                    
                    # Создаем итоговую таблицу с правильным порядком
                    analytics_df_with_total = pd.DataFrame(ordered_rows)
                    
                    # Рассчитываем общие метрики для панели
                    total_leads = analytics_df['Количество лидов'].sum()
                    total_prequalified = analytics_df['Предквалифицированные лиды'].sum()
                    total_purchased = analytics_df['Купили'].sum()
                    
                    # Средние конверсии
                    avg_lead_to_sql = round((total_prequalified / total_leads * 100), 2) if total_leads > 0 else 0
                    avg_sql_to_sale = round((total_purchased / total_prequalified * 100), 2) if total_prequalified > 0 else 0
                    
                    # Отображаем панель с метриками
                    st.subheader("📊 КЛЮЧЕВЫЕ ПОКАЗАТЕЛИ")
                    
                    # Создаем 5 колонок для метрик
                    col1, col2, col3, col4, col5 = st.columns(5)
                    
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
                        st.metric(
                            label="Конверсия Лид → SQL",
                            value=f"{avg_lead_to_sql}%",
                            help="Средняя конверсия лидов в предквалифицированные"
                        )
                    
                    with col5:
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
                    
                    st.success(f"✅ Аналитическая таблица создана! Размер: {analytics_df.shape[0]} строк, {analytics_df.shape[1]} столбцов")
                    st.info(f"📊 Анализ основан на всех {len(leads_analysis_clean)} лидах из leads2025")
                    
                    # Показываем аналитическую таблицу с итогами
                    st.subheader("📈 Аналитика лидов по месяцам:")
                    
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
