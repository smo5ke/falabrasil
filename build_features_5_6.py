import sys
import os

def update_falabrasil():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    print(f"Original length: {len(html)}")

    # 1. Add shake animation and card styles to <style>
    style_anchor = "/* Comprehensive Dark Mode Styles */"
    shake_css = """        /* Memory Game Animations & Shake */
        @keyframes shakeCard {
            0%, 100% { transform: translateX(0); }
            20%, 60% { transform: translateX(-6px); }
            40%, 80% { transform: translateX(6px); }
        }
        .animate-shake {
            animation: shakeCard 0.45s ease-in-out;
        }

        """
    if shake_css not in html:
        html = html.replace(style_anchor, shake_css + style_anchor)
        print("1. Added shake CSS")

    # 2. Add Fluency Forecast Modal
    modal_anchor = "<!-- PRONUNCIATION RULES MODAL (دليل أسرار النطق البرازيلي) -->"
    fluency_modal_html = """    <!-- FLUENCY FORECAST & MILESTONES MODAL (حاسبة وتوقع الطلاقة اللغوية والقاموس الكامل 5,000 كلمة) -->
    <div x-show="showFluencyModal" style="display: none;" class="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
        <div class="bg-white rounded-3xl p-6 sm:p-8 max-w-2xl w-full space-y-6 shadow-2xl border border-slate-100 max-h-[90vh] overflow-y-auto" @click.outside="showFluencyModal = false">
            <!-- Modal Header -->
            <div class="flex items-center justify-between border-b border-slate-100 pb-4">
                <div class="flex items-center gap-3">
                    <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr from-blue-500 to-indigo-600 flex items-center justify-center text-white text-2xl shadow-md">
                        ⏱️
                    </div>
                    <div>
                        <h3 class="font-black text-slate-900 text-lg">حاسبة وتوقع الطلاقة اللغوية</h3>
                        <p class="text-xs text-slate-400">تنبؤ زمني دقيق لمسارك الشخصي نحو إتقان 5,000 كلمة عالية التكرار</p>
                    </div>
                </div>
                <button @click="showFluencyModal = false" class="text-slate-400 hover:text-slate-600 p-1">
                    <i class="fa-solid fa-xmark text-lg"></i>
                </button>
            </div>

            <!-- Current Fluency Status Hero -->
            <div class="bg-gradient-to-r from-blue-50 via-indigo-50 to-emerald-50 p-5 rounded-2xl border border-blue-100 space-y-3">
                <div class="flex flex-wrap items-center justify-between gap-2">
                    <div>
                        <span class="text-xs font-bold text-blue-900 block">مستوى الطلاقة والفهم الحالي:</span>
                        <div class="flex items-baseline gap-2 mt-0.5">
                            <span class="text-3xl font-black text-blue-700 font-inter" x-text="getFluencyCoverage() + '%'"></span>
                            <span class="text-xs text-blue-600 font-semibold">من المحادثات اليومية في البرازيل 🇧🇷</span>
                        </div>
                    </div>
                    <div class="text-left bg-white/80 backdrop-blur px-3.5 py-2 rounded-xl border border-blue-200 shadow-sm">
                        <span class="text-[11px] text-slate-500 block font-bold">الحصيلة المتقنة:</span>
                        <span class="text-lg font-black text-emerald-600 font-inter" x-text="learnedWords.length"></span>
                        <span class="text-xs text-slate-400 font-inter" x-text="'/ ' + totalWords.toLocaleString('en-US') + ' كلمة'"></span>
                    </div>
                </div>
                <div class="w-full bg-blue-200/50 h-3 rounded-full overflow-hidden">
                    <div class="bg-gradient-to-r from-blue-500 via-indigo-500 to-emerald-500 h-full rounded-full transition-all duration-500"
                         :style="`width: ${Math.min(100, Math.max(1, (learnedWords.length / Math.max(1, totalWords)) * 100))}%`"></div>
                </div>
                <p class="text-xs text-slate-600 leading-relaxed">
                    <i class="fa-solid fa-circle-info text-blue-500 ml-1"></i>
                    كل كلمة جديدة تحفظها تقربك خطوة حقيقية من التحدث والعيش في البرازيل بثقة وسلاسة.
                </p>
            </div>

            <!-- Daily Study Pace Controller (محاكي وتيرة التعلم) -->
            <div class="bg-slate-50 p-4 rounded-2xl border border-slate-100 space-y-3">
                <div class="flex flex-wrap items-center justify-between gap-2">
                    <div>
                        <span class="text-xs font-bold text-slate-800 block">حدد وتيرة دراستك اليومية (Pace):</span>
                        <span class="text-[11px] text-slate-400">شاهد كيف تتغير تواريخ الإنجاز في الوقت الفعلي</span>
                    </div>
                    <div class="flex items-center gap-1.5 flex-wrap">
                        <template x-for="pace in [5, 10, 15, 20, 30, 50]" :key="pace">
                            <button @click="dailyGoal = pace; localStorage.setItem('fb_daily_goal', pace.toString())"
                                    :class="dailyGoal === pace ? 'bg-blue-600 text-white font-bold shadow-sm' : 'bg-white border text-slate-700 hover:bg-slate-100'"
                                    class="px-3 py-1.5 rounded-xl font-inter text-xs transition">
                                <span x-text="pace"></span> <span class="text-[10px]">ك/يوم</span>
                            </button>
                        </template>
                    </div>
                </div>

                <!-- Pace Statistics Row -->
                <div class="grid grid-cols-3 gap-2 pt-2 border-t border-slate-200/60 text-center">
                    <div class="bg-white p-2.5 rounded-xl border border-slate-200">
                        <span class="text-[10px] text-slate-400 block font-semibold">المعدل الأسبوعي</span>
                        <span class="text-sm font-black text-slate-800 font-inter" x-text="(dailyGoal * 7) + ' كلمة'"></span>
                    </div>
                    <div class="bg-white p-2.5 rounded-xl border border-slate-200">
                        <span class="text-[10px] text-slate-400 block font-semibold">المعدل الشهري</span>
                        <span class="text-sm font-black text-slate-800 font-inter" x-text="(dailyGoal * 30) + ' كلمة'"></span>
                    </div>
                    <div class="bg-white p-2.5 rounded-xl border border-slate-200">
                        <span class="text-[10px] text-slate-400 block font-semibold">الوقت اليومي المقترح</span>
                        <span class="text-sm font-black text-emerald-600 font-inter" x-text="(dailyGoal * 1.5) + ' دقيقة'"></span>
                    </div>
                </div>
            </div>

            <!-- Milestones Timeline & Forecast Cards -->
            <div class="space-y-3">
                <h4 class="text-xs font-bold text-slate-700 flex items-center gap-2">
                    <i class="fa-solid fa-flag-checkered text-emerald-600"></i>
                    <span>المحطات الرئيسية وتاريخ الوصول المتوقع لكل مستوى:</span>
                </h4>

                <div class="space-y-2.5">
                    <template x-for="m in getMilestonesList()" :key="m.code">
                        <div class="p-3.5 rounded-2xl border transition"
                             :class="m.isCompleted ? 'bg-emerald-50/70 border-emerald-200' : 'bg-white border-slate-200 hover:border-blue-200'">
                            <div class="flex items-center justify-between mb-2">
                                <div class="flex items-center gap-2">
                                    <span class="px-2.5 py-0.5 rounded-lg text-xs font-bold"
                                          :class="m.badgeClass" x-text="m.code"></span>
                                    <span class="font-bold text-xs text-slate-800" x-text="m.title"></span>
                                    <span class="text-[11px] text-slate-400 font-inter" x-text="'(' + m.targetCount.toLocaleString() + ' كلمة)'"></span>
                                </div>
                                <div class="text-left">
                                    <template x-if="m.isCompleted">
                                        <span class="inline-flex items-center gap-1 text-xs font-bold text-emerald-700 bg-emerald-100 px-2.5 py-1 rounded-xl">
                                            <i class="fa-solid fa-circle-check"></i> تم الاجتياز بنجاح! 🏆
                                        </span>
                                    </template>
                                    <template x-if="!m.isCompleted">
                                        <div class="text-left">
                                            <span class="text-xs font-bold text-blue-700 block font-inter" x-text="m.dateStr"></span>
                                            <span class="text-[10px] text-slate-400 font-inter" x-text="'متبقي ' + m.daysRemaining + ' يوم (' + m.wordsNeeded + ' كلمة)'"></span>
                                        </div>
                                    </template>
                                </div>
                            </div>

                            <!-- Progress Bar for this Milestone -->
                            <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                                <div class="h-full rounded-full transition-all duration-500"
                                     :class="m.isCompleted ? 'bg-emerald-500' : 'bg-gradient-to-r from-blue-500 to-indigo-500'"
                                     :style="`width: ${m.progressPercent}%`"></div>
                            </div>
                        </div>
                    </template>
                </div>
            </div>

            <!-- Motivational Tips Box -->
            <div class="bg-amber-50 p-3.5 rounded-2xl border border-amber-200/70 text-xs text-amber-900 flex items-start gap-3">
                <i class="fa-solid fa-lightbulb text-amber-500 text-base mt-0.5 shrink-0"></i>
                <div class="leading-relaxed">
                    <span class="font-bold block mb-0.5">نصيحة الاستمرارية الذهبية:</span>
                    الالتزام بـ <span class="font-bold" x-text="dailyGoal"></span> كلمات يومياً يجعلك تتقن اللغة أسرع بكثير من دراسة ساعات طويلة في يوم واحد ثم الانقطاع. التكرار المتباعد وسلسلة التتابع اليومية 🔥 هي سر الطلاقة الحقيقية!
                </div>
            </div>
        </div>
    </div>

    """
    if fluency_modal_html not in html:
        html = html.replace(modal_anchor, fluency_modal_html + modal_anchor)
        print("2. Added Fluency Forecast Modal")

    # 3. Add Fluency Forecast button in Header
    header_anchor = "<!-- Daily Goal Indicator & Dark Mode Toggle -->"
    header_forecast_btn = """<!-- Fluency Forecast Button & Daily Goal & Dark Mode -->
                <div class="hidden lg:flex items-center gap-2.5">
                    <!-- Fluency Forecast Pill Button -->
                    <button @click="showFluencyModal = true" class="cursor-pointer flex items-center gap-2 px-3 py-1.5 rounded-2xl border text-xs font-bold transition shadow-sm bg-gradient-to-r from-blue-500/10 to-indigo-500/10 border-blue-200 text-blue-700 hover:from-blue-500/20 hover:to-indigo-500/20" title="حاسبة وتوقع الطلاقة والوصول لـ 5,000 كلمة">
                        <i class="fa-solid fa-chart-line text-blue-600"></i>
                        <span>توقع الطلاقة ⏱️</span>
                    </button>
"""
    if "توقع الطلاقة ⏱️" not in html:
        html = html.replace(header_anchor, header_forecast_btn)
        print("3. Added Fluency Forecast button to header")

    # 4. Add Fluency Forecast trigger button in Profile Modal
    profile_rank_anchor = "<!-- Rank Progress Bar -->"
    profile_forecast_btn = """<!-- Fluency Forecast Trigger in Profile Modal -->
            <button @click="showProfileModal = false; showFluencyModal = true" class="w-full py-2.5 px-3 bg-gradient-to-r from-blue-50 to-indigo-50 hover:from-blue-100 hover:to-indigo-100 text-blue-800 border border-blue-200 font-bold rounded-2xl text-xs transition flex items-center justify-center gap-2">
                <i class="fa-solid fa-chart-line text-blue-600"></i>
                <span>عرض حاسبة الطلاقة والتنبؤ الزمني (5k Roadmap) ⏱️</span>
            </button>

            """
    if "عرض حاسبة الطلاقة والتنبؤ الزمني" not in html:
        html = html.replace(profile_rank_anchor, profile_forecast_btn + profile_rank_anchor)
        print("4. Added Fluency trigger to Profile Modal")

    # 5. Add Interactive Fluency Forecast Widget in Stages Tab
    stages_anchor = "<!-- Stage Cards Grid -->"
    stages_widget_html = """<!-- Interactive Fluency Forecast Widget Banner -->
            <div class="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm hover:shadow-md transition">
                <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                    <div class="flex items-center gap-4">
                        <div class="w-14 h-14 rounded-2xl bg-gradient-to-tr from-blue-500 to-indigo-600 text-white flex items-center justify-center text-2xl shadow-md shrink-0">
                            ⏱️
                        </div>
                        <div>
                            <div class="flex items-center gap-2">
                                <h3 class="font-black text-slate-900 text-lg">حاسبة وتوقع الطلاقة اللغوية (5k Roadmap)</h3>
                                <span class="bg-blue-100 text-blue-800 text-xs px-2.5 py-0.5 rounded-full font-bold">ذكية وتفاعلية</span>
                            </div>
                            <p class="text-xs text-slate-500 mt-1">
                                معدل حصيلتك الحالية <span class="font-bold text-emerald-600 font-inter" x-text="learnedWords.length"></span> كلمة تمنحك فهماً لـ <span class="font-bold text-blue-600 font-inter" x-text="getFluencyCoverage() + '%'"></span> من المحادثات اليومية في البرازيل.
                            </p>
                        </div>
                    </div>
                    <div class="flex items-center gap-2 w-full md:w-auto justify-end">
                        <button @click="showFluencyModal = true" class="px-5 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold rounded-2xl text-xs sm:text-sm shadow-md shadow-blue-500/20 transition flex items-center gap-2">
                            <i class="fa-solid fa-chart-line"></i>
                            <span>فتح حاسبة وخريطة الوصول الكاملة</span>
                        </button>
                    </div>
                </div>

                <!-- Quick Pace Bar in Widget -->
                <div class="mt-5 pt-4 border-t border-slate-100 flex flex-wrap items-center justify-between gap-3 text-xs">
                    <div class="flex items-center gap-2">
                        <span class="text-slate-600 font-bold">هدفك اليومي الحالي:</span>
                        <span class="px-2.5 py-1 bg-blue-50 text-blue-700 font-inter font-bold rounded-xl border border-blue-200" x-text="dailyGoal + ' كلمات/يوم'"></span>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="text-slate-500">التاريخ المتوقع لختم القاموس الكامل بالكامل:</span>
                        <span class="font-bold text-indigo-700 font-inter" x-text="getMilestoneForecast(Math.max(1, totalWords)).dateStr"></span>
                        <span class="text-[11px] text-slate-400 font-inter" x-text="'(خلال ' + getMilestoneForecast(Math.max(1, totalWords)).daysRemaining + ' يوم)'"></span>
                    </div>
                </div>
            </div>

            """
    if stages_widget_html not in html:
        html = html.replace(stages_anchor, stages_widget_html + stages_anchor)
        print("5. Added Fluency Widget to Stages tab")

    # 6. Add Memory Match Game Section
    dict_tab_anchor = "<!-- TAB 4: FULL DICTIONARY"
    memory_section_html = """<!-- TAB: MEMORY MATCH GAME (لعبة الذاكرة ومطابقة الكلمات السريعة) -->
        <section x-show="activeTab === 'memory_game'" class="max-w-4xl mx-auto space-y-6">
            <!-- Game Header & Controls Card -->
            <div class="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm space-y-5">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div class="flex items-center gap-3">
                        <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr from-purple-500 to-indigo-600 text-white flex items-center justify-center text-2xl shadow-md">
                            🧩
                        </div>
                        <div>
                            <h2 class="font-black text-xl text-slate-900">لعبة الذاكرة ومطابقة الكلمات (Memory Match)</h2>
                            <p class="text-xs text-slate-500">طابق بين الكلمة البرتغالية وترجمتها العربية بأسرع وقت وأقل عدد حركات!</p>
                        </div>
                    </div>

                    <!-- Action Buttons -->
                    <div class="flex items-center gap-2">
                        <button @click="restartMemoryGame()" class="px-4 py-2.5 bg-purple-600 hover:bg-purple-700 text-white font-bold rounded-2xl text-xs transition flex items-center gap-2 shadow-sm shadow-purple-600/20 active:scale-95">
                            <i class="fa-solid fa-rotate-right"></i>
                            <span>جولة جديدة 🔄</span>
                        </button>
                    </div>
                </div>

                <!-- Game Settings & Filters Row -->
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-4 border-t border-slate-100 text-xs">
                    <!-- Stage / Level Filter -->
                    <div>
                        <label class="block font-bold text-slate-700 mb-1.5">مستوى الكلمات:</label>
                        <select x-model="memoryLevel" @change="restartMemoryGame()" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-semibold focus:outline-none focus:border-purple-500">
                            <option value="ALL">جميع المستويات (5,000 كلمة)</option>
                            <option value="A1">المستوى A1 (الكلمات 1 - 500)</option>
                            <option value="A2">المستوى A2 (الكلمات 501 - 1,300)</option>
                            <option value="B1">المستوى B1 (الكلمات 1,301 - 2,300)</option>
                            <option value="B2">المستوى B2 (الكلمات 2,301 - 3,400)</option>
                            <option value="C1/C2">المستويان C1+C2 (الكلمات 3,401 - 5,000)</option>
                            <option value="DIFFICULT">كلماتي الصعبة فقط ⚠️</option>
                        </select>
                    </div>

                    <!-- Game Mode (Flip vs Speed Match) -->
                    <div>
                        <label class="block font-bold text-slate-700 mb-1.5">نمط التحدي:</label>
                        <div class="flex rounded-xl bg-slate-100 p-1 border border-slate-200">
                            <button @click="setMemoryMode('flip')"
                                    :class="memoryMode === 'flip' ? 'bg-white text-purple-700 font-bold shadow-sm' : 'text-slate-600'"
                                    class="flex-1 py-1.5 text-center rounded-lg transition text-xs flex items-center justify-center gap-1">
                                <span>🃏 كشف الذاكرة</span>
                            </button>
                            <button @click="setMemoryMode('speed')"
                                    :class="memoryMode === 'speed' ? 'bg-white text-purple-700 font-bold shadow-sm' : 'text-slate-600'"
                                    class="flex-1 py-1.5 text-center rounded-lg transition text-xs flex items-center justify-center gap-1">
                                <span>⚡ مطابقة سريعة</span>
                            </button>
                        </div>
                    </div>

                    <!-- Grid Size (Pairs) -->
                    <div>
                        <label class="block font-bold text-slate-700 mb-1.5">حجم التحدي:</label>
                        <div class="flex rounded-xl bg-slate-100 p-1 border border-slate-200">
                            <button @click="setMemoryPairsCount(6)"
                                    :class="memoryTotalPairs === 6 ? 'bg-white text-purple-700 font-bold shadow-sm' : 'text-slate-600'"
                                    class="flex-1 py-1.5 text-center rounded-lg transition text-xs">
                                <span>6 أزواج (12 بطاقة)</span>
                            </button>
                            <button @click="setMemoryPairsCount(8)"
                                    :class="memoryTotalPairs === 8 ? 'bg-white text-purple-700 font-bold shadow-sm' : 'text-slate-600'"
                                    class="flex-1 py-1.5 text-center rounded-lg transition text-xs">
                                <span>8 أزواج (16 بطاقة)</span>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Live Gameplay Dashboard Stats Bar -->
                <div class="grid grid-cols-4 gap-2 pt-2 text-center text-xs">
                    <div class="bg-purple-50/70 border border-purple-100 rounded-2xl p-2.5">
                        <span class="text-[10px] text-purple-700 font-semibold block">المؤقت الزمني ⏱️</span>
                        <span class="text-base font-black text-purple-800 font-inter" x-text="formatGameTime(memoryGameTime)"></span>
                    </div>
                    <div class="bg-indigo-50/70 border border-indigo-100 rounded-2xl p-2.5">
                        <span class="text-[10px] text-indigo-700 font-semibold block">الحركات 🔄</span>
                        <span class="text-base font-black text-indigo-800 font-inter" x-text="memoryGameMoves"></span>
                    </div>
                    <div class="bg-emerald-50/70 border border-emerald-100 rounded-2xl p-2.5">
                        <span class="text-[10px] text-emerald-700 font-semibold block">المطابقات ✅</span>
                        <span class="text-base font-black text-emerald-800 font-inter" x-text="memoryMatchedPairs + ' / ' + memoryTotalPairs"></span>
                    </div>
                    <div class="bg-amber-50/70 border border-amber-100 rounded-2xl p-2.5">
                        <span class="text-[10px] text-amber-700 font-semibold block">نقاط الجولة ⭐</span>
                        <span class="text-base font-black text-amber-800 font-inter" x-text="'+' + memoryGameXp + ' XP'"></span>
                    </div>
                </div>
            </div>

            <!-- Victory Card Overlay (عند إتمام المطابقات بنجاح) -->
            <div x-show="memoryGameCompleted" x-transition class="bg-gradient-to-r from-emerald-600 to-teal-700 rounded-3xl p-6 sm:p-8 text-white shadow-xl text-center space-y-4">
                <div class="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center text-3xl mx-auto shadow-inner">
                    🎉
                </div>
                <h3 class="text-2xl font-black">أحسنت صنعاً! أتممت الجولة بنجاح! 🏆</h3>
                <p class="text-emerald-100 text-sm max-w-md mx-auto">
                    تمت مطابقة جميع الكلمات وحصلت على <span class="font-bold text-amber-300 font-inter">+<span x-text="memoryGameXp"></span> XP</span> أضيفت لحسابك الشخصي!
                </p>

                <!-- Victory Stats Grid -->
                <div class="grid grid-cols-3 gap-3 max-w-sm mx-auto bg-white/10 backdrop-blur rounded-2xl p-3 text-xs font-inter">
                    <div>
                        <span class="text-emerald-200 block text-[10px]">الوقت</span>
                        <span class="text-lg font-bold" x-text="formatGameTime(memoryGameTime)"></span>
                    </div>
                    <div>
                        <span class="text-emerald-200 block text-[10px]">الحركات</span>
                        <span class="text-lg font-bold" x-text="memoryGameMoves"></span>
                    </div>
                    <div>
                        <span class="text-emerald-200 block text-[10px]">الدقة</span>
                        <span class="text-lg font-bold" x-text="Math.round((memoryTotalPairs / Math.max(memoryTotalPairs, memoryGameMoves)) * 100) + '%'"></span>
                    </div>
                </div>

                <div class="flex justify-center gap-3 pt-2">
                    <button @click="restartMemoryGame()" class="bg-amber-400 hover:bg-amber-300 text-slate-900 font-bold px-6 py-3 rounded-2xl shadow-lg transition active:scale-95 flex items-center gap-2 text-sm">
                        <i class="fa-solid fa-rotate-right"></i>
                        <span>العب جولة جديدة بكلمات مختلفة</span>
                    </button>
                    <button @click="activeTab = 'flashcards'" class="bg-white/10 hover:bg-white/20 text-white font-bold px-5 py-3 rounded-2xl transition text-sm">
                        <span>مراجعة البطاقات</span>
                    </button>
                </div>
            </div>

            <!-- Empty State for Difficult Words if none -->
            <div x-show="memoryCards.length === 0 && memoryLevel === 'DIFFICULT'" class="bg-white rounded-3xl p-8 border border-slate-200 text-center space-y-3">
                <div class="text-4xl">⭐</div>
                <h4 class="font-bold text-slate-800">قائمة الكلمات الصعبة فارغة حالياً!</h4>
                <p class="text-xs text-slate-500">قم بوضع علامة "صعبة" على أي كلمة أثناء ممارسة البطاقات لتتدرب عليها هنا.</p>
                <button @click="memoryLevel = 'ALL'; restartMemoryGame()" class="px-4 py-2 bg-purple-600 text-white rounded-xl text-xs font-bold">
                    التبديل إلى جميع الكلمات
                </button>
            </div>

            <!-- The Interactive Cards Grid -->
            <div x-show="memoryCards.length > 0" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3 sm:gap-4">
                <template x-for="card in memoryCards" :key="card.id">
                    <div @click="handleMemoryCardClick(card)"
                         class="relative h-28 sm:h-32 rounded-2xl border-2 transition-all duration-300 select-none cursor-pointer flex flex-col items-center justify-center p-3 text-center"
                         :class="{
                             'bg-emerald-500 border-emerald-400 text-white shadow-md shadow-emerald-500/20 scale-[0.98]': card.isMatched,
                             'bg-purple-600 border-purple-500 text-white shadow-lg ring-2 ring-purple-300': (memorySelectedCard1 && memorySelectedCard1.id === card.id) || (memorySelectedCard2 && memorySelectedCard2.id === card.id),
                             'bg-red-500 border-red-400 text-white animate-shake': card.isError,
                             'bg-white border-slate-200 hover:border-purple-300 hover:shadow-md': !card.isMatched && !card.isError && (memoryMode === 'speed' || card.isFlipped),
                             'bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700 hover:border-purple-400 text-white hover:scale-[1.02]': !card.isMatched && !card.isError && memoryMode === 'flip' && !card.isFlipped
                         }">

                        <!-- Face Down State (Flip Mode Hidden) -->
                        <div x-show="memoryMode === 'flip' && !card.isFlipped && !card.isMatched" class="flex flex-col items-center gap-1.5 pointer-events-none">
                            <span class="text-2xl">🇧🇷</span>
                            <span class="text-[10px] font-bold text-slate-400 tracking-wider">FALABRASIL</span>
                        </div>

                        <!-- Face Up / Open Card Content -->
                        <div x-show="memoryMode === 'speed' || card.isFlipped || card.isMatched" class="w-full flex flex-col items-center justify-center pointer-events-none">
                            <!-- Type Badge (PT vs AR) -->
                            <div class="flex items-center justify-between w-full mb-1">
                                <span class="text-[9px] font-bold px-1.5 py-0.5 rounded uppercase"
                                      :class="card.type === 'pt' ? 'bg-emerald-100 text-emerald-800' : 'bg-blue-100 text-blue-800'"
                                      x-text="card.type === 'pt' ? '🇧🇷 برتغالي' : '🇸🇦 عربي'"></span>

                                <template x-if="card.isMatched">
                                    <i class="fa-solid fa-circle-check text-xs text-white"></i>
                                </template>
                                <template x-if="card.type === 'pt' && !card.isMatched">
                                    <i class="fa-solid fa-volume-high text-[10px] text-slate-400"></i>
                                </template>
                            </div>

                            <!-- Word Text -->
                            <p class="font-black leading-tight line-clamp-2"
                               :class="{
                                   'text-white': card.isMatched || card.isError || ((memorySelectedCard1 && memorySelectedCard1.id === card.id) || (memorySelectedCard2 && memorySelectedCard2.id === card.id)),
                                   'text-slate-900': !card.isMatched && !card.isError && !(memorySelectedCard1 && memorySelectedCard1.id === card.id),
                                   'text-base sm:text-lg font-inter': card.type === 'pt',
                                   'text-sm sm:text-base font-cairo': card.type === 'ar'
                               }"
                               x-text="card.text"></p>
                        </div>
                    </div>
                </template>
            </div>
        </section>

        """
    if memory_section_html not in html:
        html = html.replace(dict_tab_anchor, memory_section_html + dict_tab_anchor)
        print("6. Added Memory Match Game section")

    # 7. Add Memory Match tab into tabs array in Alpine.js
    old_tabs = """                tabs: [
                    { id: 'stages', name: 'المراحل وخطة التعلم', icon: 'fa-solid fa-map-location-dot' },
                    { id: 'flashcards', name: 'البطاقات التعليمية', icon: 'fa-solid fa-clone' },
                    { id: 'quiz', name: 'ساحة التحديات', icon: 'fa-solid fa-gamepad' },
                    { id: 'dictionary', name: 'القاموس الشامل', icon: 'fa-solid fa-book-open' },"""

    new_tabs = """                tabs: [
                    { id: 'stages', name: 'المراحل وخطة التعلم', icon: 'fa-solid fa-map-location-dot' },
                    { id: 'flashcards', name: 'البطاقات التعليمية', icon: 'fa-solid fa-clone' },
                    { id: 'quiz', name: 'ساحة التحديات', icon: 'fa-solid fa-gamepad' },
                    { id: 'memory_game', name: 'لعبة الذاكرة 🧩', icon: 'fa-solid fa-puzzle-piece' },
                    { id: 'dictionary', name: 'القاموس الشامل', icon: 'fa-solid fa-book-open' },"""

    if old_tabs in html:
        html = html.replace(old_tabs, new_tabs)
        print("7. Added memory_game to tabs array")

    # 8. Add Alpine.js State variables for Fluency Forecast & Memory Game
    state_anchor = "showProfileModal: false,"
    new_state = """showProfileModal: false,
                showFluencyModal: false,

                // Memory Game State (لعبة الذاكرة ومطابقة الكلمات)
                memoryLevel: 'ALL',
                memoryMode: 'flip',
                memoryTotalPairs: 6,
                memoryCards: [],
                memorySelectedCard1: null,
                memorySelectedCard2: null,
                memoryMatchedPairs: 0,
                memoryGameMoves: 0,
                memoryGameTime: 0,
                memoryTimerInterval: null,
                memoryBoardLocked: false,
                memoryGameCompleted: false,
                memoryGameXp: 0,
"""
    if "showFluencyModal: false" not in html:
        html = html.replace(state_anchor, new_state)
        print("8. Added Alpine state variables")

    # 9. Add Alpine.js Methods for Fluency Forecast & Memory Game
    methods_anchor = "saveProgress() {"
    new_methods = """// FLUENCY FORECAST CALCULATIONS
                getFluencyCoverage() {
                    const count = this.learnedWords.length;
                    if (count <= 0) return 10;
                    if (count < 500) return Math.round(10 + (count / 500) * 65);
                    if (count < 1300) return Math.round(75 + ((count - 500) / 800) * 10);
                    if (count < 2300) return Math.round(85 + ((count - 1300) / 1000) * 7);
                    if (count < 3400) return Math.round(92 + ((count - 2300) / 1100) * 4);
                    if (count < 5000) return Math.round(96 + ((count - 3400) / 1600) * 3);
                    return 99;
                },

                getMilestoneForecast(targetCount) {
                    const learned = this.learnedWords.length;
                    const needed = Math.max(0, targetCount - learned);
                    const pace = Math.max(1, this.dailyGoal || 10);
                    const days = Math.ceil(needed / pace);
                    const isCompleted = needed === 0;

                    const targetDate = new Date(Date.now() + days * 86400000);
                    const dateStr = targetDate.toLocaleDateString('ar-EG', { year: 'numeric', month: 'short', day: 'numeric' });

                    return {
                        targetCount,
                        learned,
                        wordsNeeded: needed,
                        daysRemaining: days,
                        isCompleted,
                        dateStr,
                        progressPercent: Math.min(100, Math.round((learned / targetCount) * 100))
                    };
                },

                getMilestonesList() {
                    const list = [
                        { code: 'A1', title: 'مبتدئ أساسي (فهم 75% من الكلام اليومي)', targetCount: 500, badgeClass: 'bg-emerald-100 text-emerald-800' },
                        { code: 'A2', title: 'مبتدئ متقدم (التسوق، السفر والروتين 85%)', targetCount: 1300, badgeClass: 'bg-cyan-100 text-cyan-800' },
                        { code: 'B1', title: 'مستوى متوسط (استقلالية وحوارات العمل 92%)', targetCount: 2300, badgeClass: 'bg-amber-100 text-amber-800' },
                        { code: 'B2', title: 'فوق المتوسط (طلاقة ومفردات مركبة 96%)', targetCount: 3400, badgeClass: 'bg-orange-100 text-orange-800' },
                        { code: 'C1/C2', title: 'الطلاقة التامة وإتقان القاموس الكامل (99%+)', targetCount: 5000, badgeClass: 'bg-purple-100 text-purple-800' },
                    ];

                    return list.map(item => {
                        const forecast = this.getMilestoneForecast(item.targetCount);
                        return { ...item, ...forecast };
                    });
                },

                // MEMORY MATCH GAME METHODS
                setMemoryMode(mode) {
                    this.memoryMode = mode;
                    this.restartMemoryGame();
                },

                setMemoryPairsCount(count) {
                    this.memoryTotalPairs = count;
                    this.restartMemoryGame();
                },

                formatGameTime(seconds) {
                    const mins = Math.floor(seconds / 60);
                    const secs = seconds % 60;
                    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
                },

                startMemoryTimer() {
                    clearInterval(this.memoryTimerInterval);
                    this.memoryGameTime = 0;
                    this.memoryTimerInterval = setInterval(() => {
                        if (!this.memoryGameCompleted) {
                            this.memoryGameTime++;
                        }
                    }, 1000);
                },

                restartMemoryGame() {
                    clearInterval(this.memoryTimerInterval);
                    this.memorySelectedCard1 = null;
                    this.memorySelectedCard2 = null;
                    this.memoryMatchedPairs = 0;
                    this.memoryGameMoves = 0;
                    this.memoryBoardLocked = false;
                    this.memoryGameCompleted = false;
                    this.memoryGameXp = 0;

                    let pool = [];
                    if (this.memoryLevel === 'DIFFICULT') {
                        pool = this.fullDictionary.filter(w => this.difficultWords.includes(w.id));
                    } else if (this.memoryLevel === 'ALL') {
                        pool = this.fullDictionary;
                    } else if (this.memoryLevel === 'C1/C2') {
                        pool = this.fullDictionary.filter(w => w.level === 'C1/C2' || w.level === 'C1' || w.level === 'C2');
                    } else {
                        pool = this.fullDictionary.filter(w => w.level === this.memoryLevel);
                    }

                    if (!pool || pool.length === 0) {
                        if (this.memoryLevel === 'DIFFICULT') {
                            this.memoryCards = [];
                            return;
                        }
                        pool = this.fullDictionary.slice(0, 50);
                    }

                    if (!pool || pool.length === 0) {
                        this.memoryCards = [];
                        return;
                    }

                    const shuffledPool = [...pool].sort(() => 0.5 - Math.random());
                    const selectedWords = shuffledPool.slice(0, this.memoryTotalPairs);

                    const cards = [];
                    selectedWords.forEach((w, idx) => {
                        const pairId = 'pair_' + idx;
                        cards.push({
                            id: 'pt_' + idx + '_' + Math.random().toString(36).substr(2, 4),
                            pairId: pairId,
                            type: 'pt',
                            text: w.word,
                            word: w.word,
                            translation: w.translation,
                            isFlipped: this.memoryMode === 'speed',
                            isMatched: false,
                            isError: false
                        });
                        cards.push({
                            id: 'ar_' + idx + '_' + Math.random().toString(36).substr(2, 4),
                            pairId: pairId,
                            type: 'ar',
                            text: w.translation,
                            word: w.word,
                            translation: w.translation,
                            isFlipped: this.memoryMode === 'speed',
                            isMatched: false,
                            isError: false
                        });
                    });

                    this.memoryCards = cards.sort(() => 0.5 - Math.random());
                    this.startMemoryTimer();
                },

                handleMemoryCardClick(card) {
                    if (card.isMatched || this.memoryBoardLocked || this.memoryGameCompleted) return;

                    if (this.memoryMode === 'flip') {
                        if (card.isFlipped) return;
                        card.isFlipped = true;

                        if (card.type === 'pt') {
                            this.speak(card.word);
                        }

                        if (!this.memorySelectedCard1) {
                            this.memorySelectedCard1 = card;
                        } else if (!this.memorySelectedCard2) {
                            this.memorySelectedCard2 = card;
                            this.memoryGameMoves++;
                            this.evaluateMemoryPair();
                        }
                    } else {
                        if (card.type === 'pt') {
                            this.speak(card.word);
                        }

                        if (!this.memorySelectedCard1) {
                            this.memorySelectedCard1 = card;
                        } else if (this.memorySelectedCard1.id === card.id) {
                            this.memorySelectedCard1 = null;
                        } else if (this.memorySelectedCard1.type === card.type) {
                            this.memorySelectedCard1 = card;
                        } else {
                            this.memorySelectedCard2 = card;
                            this.memoryGameMoves++;
                            this.evaluateMemoryPair();
                        }
                    }
                },

                evaluateMemoryPair() {
                    const card1 = this.memorySelectedCard1;
                    const card2 = this.memorySelectedCard2;

                    if (card1.pairId === card2.pairId) {
                        card1.isMatched = true;
                        card2.isMatched = true;
                        this.memoryMatchedPairs++;
                        this.memoryGameXp += 15;
                        this.xp += 15;
                        this.saveProgress();

                        this.speak(card1.word);

                        this.memorySelectedCard1 = null;
                        this.memorySelectedCard2 = null;

                        if (this.memoryMatchedPairs === this.memoryTotalPairs) {
                            clearInterval(this.memoryTimerInterval);
                            this.memoryGameCompleted = true;
                            this.memoryGameXp += 50;
                            this.xp += 50;
                            this.saveProgress();
                            this.showToast('مبروك! أتممت شبكة المطابقة بنجاح وحصلت على +50 XP مكافأة! 🎉', 'success');
                        }
                    } else {
                        this.memoryBoardLocked = true;
                        card1.isError = true;
                        card2.isError = true;

                        setTimeout(() => {
                            if (this.memoryMode === 'flip') {
                                card1.isFlipped = false;
                                card2.isFlipped = false;
                            }
                            card1.isError = false;
                            card2.isError = false;
                            this.memorySelectedCard1 = null;
                            this.memorySelectedCard2 = null;
                            this.memoryBoardLocked = false;
                        }, 800);
                    }
                },

                """
    if "// FLUENCY FORECAST CALCULATIONS" not in html:
        html = html.replace(methods_anchor, new_methods + methods_anchor)
        print("9. Added Fluency Forecast & Memory Game methods")

    # 10. Update navbar template @click so clicking memory_game auto initializes it (desktop + mobile)
    old_nav_click = '@click="activeTab = tab.id"'
    new_nav_click = '@click="activeTab = tab.id; if (tab.id === \'memory_game\' && memoryCards.length === 0) restartMemoryGame()"'
    if old_nav_click in html:
        html = html.replace(old_nav_click, new_nav_click)
        print("10. Updated desktop nav clicks for automatic card dealing")

    old_nav_click_mobile = '@click="activeTab = tab.id; mobileMenuOpen = false"'
    new_nav_click_mobile = '@click="activeTab = tab.id; mobileMenuOpen = false; if (tab.id === \'memory_game\' && memoryCards.length === 0) restartMemoryGame()"'
    if old_nav_click_mobile in html:
        html = html.replace(old_nav_click_mobile, new_nav_click_mobile)
        print("10b. Updated mobile nav clicks for automatic card dealing")

    # Write to index.html only (falabrasil.html duplicate was removed in a869860)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("Success! index.html updated.")
    print(f"New length: {len(html)}")

if __name__ == '__main__':
    update_falabrasil()

