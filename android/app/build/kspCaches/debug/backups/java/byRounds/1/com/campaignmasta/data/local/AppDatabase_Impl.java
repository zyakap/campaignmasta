package com.campaignmasta.data.local;

import androidx.annotation.NonNull;
import androidx.room.DatabaseConfiguration;
import androidx.room.InvalidationTracker;
import androidx.room.RoomDatabase;
import androidx.room.RoomOpenHelper;
import androidx.room.migration.AutoMigrationSpec;
import androidx.room.migration.Migration;
import androidx.room.util.DBUtil;
import androidx.room.util.TableInfo;
import androidx.sqlite.db.SupportSQLiteDatabase;
import androidx.sqlite.db.SupportSQLiteOpenHelper;
import com.campaignmasta.data.local.dao.CallLogDao;
import com.campaignmasta.data.local.dao.CallLogDao_Impl;
import com.campaignmasta.data.local.dao.CommunityGroupDao;
import com.campaignmasta.data.local.dao.CommunityGroupDao_Impl;
import com.campaignmasta.data.local.dao.InfluencerDao;
import com.campaignmasta.data.local.dao.InfluencerDao_Impl;
import com.campaignmasta.data.local.dao.MessageDao;
import com.campaignmasta.data.local.dao.MessageDao_Impl;
import com.campaignmasta.data.local.dao.PollingLocationDao;
import com.campaignmasta.data.local.dao.PollingLocationDao_Impl;
import com.campaignmasta.data.local.dao.SupporterDao;
import com.campaignmasta.data.local.dao.SupporterDao_Impl;
import com.campaignmasta.data.local.dao.SyncQueueDao;
import com.campaignmasta.data.local.dao.SyncQueueDao_Impl;
import com.campaignmasta.data.local.dao.TeamMemberDao;
import com.campaignmasta.data.local.dao.TeamMemberDao_Impl;
import com.campaignmasta.data.local.dao.WardProfileDao;
import com.campaignmasta.data.local.dao.WardProfileDao_Impl;
import java.lang.Class;
import java.lang.Override;
import java.lang.String;
import java.lang.SuppressWarnings;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import javax.annotation.processing.Generated;

@Generated("androidx.room.RoomProcessor")
@SuppressWarnings({"unchecked", "deprecation"})
public final class AppDatabase_Impl extends AppDatabase {
  private volatile SupporterDao _supporterDao;

  private volatile CallLogDao _callLogDao;

  private volatile MessageDao _messageDao;

  private volatile TeamMemberDao _teamMemberDao;

  private volatile InfluencerDao _influencerDao;

  private volatile WardProfileDao _wardProfileDao;

  private volatile CommunityGroupDao _communityGroupDao;

  private volatile PollingLocationDao _pollingLocationDao;

  private volatile SyncQueueDao _syncQueueDao;

  @Override
  @NonNull
  protected SupportSQLiteOpenHelper createOpenHelper(@NonNull final DatabaseConfiguration config) {
    final SupportSQLiteOpenHelper.Callback _openCallback = new RoomOpenHelper(config, new RoomOpenHelper.Delegate(1) {
      @Override
      public void createAllTables(@NonNull final SupportSQLiteDatabase db) {
        db.execSQL("CREATE TABLE IF NOT EXISTS `supporters` (`localId` TEXT NOT NULL, `serverId` INTEGER, `fullName` TEXT NOT NULL, `gender` TEXT NOT NULL, `ageRange` TEXT NOT NULL, `phone` TEXT NOT NULL, `ward` TEXT NOT NULL, `wardId` INTEGER, `village` TEXT NOT NULL, `villageId` INTEGER, `clan` TEXT NOT NULL, `enrollmentStatus` TEXT NOT NULL, `supportStatus` TEXT NOT NULL, `notes` TEXT NOT NULL, `followUpRequired` INTEGER NOT NULL, `followUpDate` TEXT, `consentToMessages` INTEGER NOT NULL, `updatedAt` TEXT NOT NULL, `syncStatus` TEXT NOT NULL, `createdLocallyAt` INTEGER NOT NULL, PRIMARY KEY(`localId`))");
        db.execSQL("CREATE INDEX IF NOT EXISTS `index_supporters_serverId` ON `supporters` (`serverId`)");
        db.execSQL("CREATE INDEX IF NOT EXISTS `index_supporters_syncStatus` ON `supporters` (`syncStatus`)");
        db.execSQL("CREATE TABLE IF NOT EXISTS `call_logs` (`localId` TEXT NOT NULL, `serverId` INTEGER, `personCalled` TEXT NOT NULL, `personType` TEXT NOT NULL, `phoneNumber` TEXT NOT NULL, `callDatetime` TEXT NOT NULL, `callOutcome` TEXT NOT NULL, `discussionSummary` TEXT NOT NULL, `issuesRaised` TEXT NOT NULL, `commitmentsMade` TEXT NOT NULL, `followUpRequired` INTEGER NOT NULL, `followUpDate` TEXT, `influencerId` INTEGER, `supporterId` INTEGER, `callerId` INTEGER, `updatedAt` TEXT NOT NULL, `syncStatus` TEXT NOT NULL, `createdLocallyAt` INTEGER NOT NULL, PRIMARY KEY(`localId`))");
        db.execSQL("CREATE INDEX IF NOT EXISTS `index_call_logs_serverId` ON `call_logs` (`serverId`)");
        db.execSQL("CREATE INDEX IF NOT EXISTS `index_call_logs_syncStatus` ON `call_logs` (`syncStatus`)");
        db.execSQL("CREATE TABLE IF NOT EXISTS `messages` (`localId` TEXT NOT NULL, `serverId` INTEGER, `subject` TEXT NOT NULL, `body` TEXT NOT NULL, `messageType` TEXT NOT NULL, `priority` TEXT NOT NULL, `senderName` TEXT NOT NULL, `deliveryChannel` TEXT NOT NULL, `status` TEXT NOT NULL, `sentAt` TEXT, `isRead` INTEGER NOT NULL, `isAcknowledged` INTEGER NOT NULL, `readReceiptRequired` INTEGER NOT NULL, `acknowledgementRequired` INTEGER NOT NULL, `updatedAt` TEXT NOT NULL, `readSyncStatus` TEXT NOT NULL, `ackSyncStatus` TEXT NOT NULL, PRIMARY KEY(`localId`))");
        db.execSQL("CREATE INDEX IF NOT EXISTS `index_messages_serverId` ON `messages` (`serverId`)");
        db.execSQL("CREATE TABLE IF NOT EXISTS `team_members` (`localId` TEXT NOT NULL, `serverId` INTEGER NOT NULL, `fullName` TEXT NOT NULL, `gender` TEXT NOT NULL, `phone` TEXT NOT NULL, `email` TEXT NOT NULL, `role` TEXT NOT NULL, `wardName` TEXT NOT NULL, `wardId` INTEGER, `isActive` INTEGER NOT NULL, `notes` TEXT NOT NULL, `updatedAt` TEXT NOT NULL, PRIMARY KEY(`localId`))");
        db.execSQL("CREATE INDEX IF NOT EXISTS `index_team_members_serverId` ON `team_members` (`serverId`)");
        db.execSQL("CREATE TABLE IF NOT EXISTS `influencers` (`localId` TEXT NOT NULL, `serverId` INTEGER NOT NULL, `fullName` TEXT NOT NULL, `phone` TEXT NOT NULL, `communityRole` TEXT NOT NULL, `influenceLevel` TEXT NOT NULL, `relationshipStatus` TEXT NOT NULL, `contactFrequencyDays` INTEGER NOT NULL, `lastCallDate` TEXT, `nextContactDueDate` TEXT, `wardName` TEXT NOT NULL, `wardId` INTEGER, `notes` TEXT NOT NULL, `updatedAt` TEXT NOT NULL, PRIMARY KEY(`localId`))");
        db.execSQL("CREATE INDEX IF NOT EXISTS `index_influencers_serverId` ON `influencers` (`serverId`)");
        db.execSQL("CREATE TABLE IF NOT EXISTS `ward_profiles` (`localId` TEXT NOT NULL, `serverId` INTEGER NOT NULL, `wardId` INTEGER NOT NULL, `wardName` TEXT NOT NULL, `wardNumber` TEXT NOT NULL, `llgName` TEXT NOT NULL, `councillorName` TEXT NOT NULL, `supportStrength` TEXT NOT NULL, `populationEstimate` INTEGER, `estimatedVotingPopulation` INTEGER, `keyClans` TEXT NOT NULL, `keyChurches` TEXT NOT NULL, `mainCommunityIssues` TEXT NOT NULL, `notesForCandidate` TEXT NOT NULL, `securityConcerns` TEXT NOT NULL, `updatedAt` TEXT NOT NULL, PRIMARY KEY(`localId`))");
        db.execSQL("CREATE INDEX IF NOT EXISTS `index_ward_profiles_serverId` ON `ward_profiles` (`serverId`)");
        db.execSQL("CREATE TABLE IF NOT EXISTS `community_groups` (`localId` TEXT NOT NULL, `serverId` INTEGER, `name` TEXT NOT NULL, `groupType` TEXT NOT NULL, `wardName` TEXT NOT NULL, `wardId` INTEGER, `estimatedVotingMembers` INTEGER, `alignment` TEXT NOT NULL, `notes` TEXT NOT NULL, `updatedAt` TEXT NOT NULL, `syncStatus` TEXT NOT NULL, PRIMARY KEY(`localId`))");
        db.execSQL("CREATE INDEX IF NOT EXISTS `index_community_groups_serverId` ON `community_groups` (`serverId`)");
        db.execSQL("CREATE INDEX IF NOT EXISTS `index_community_groups_syncStatus` ON `community_groups` (`syncStatus`)");
        db.execSQL("CREATE TABLE IF NOT EXISTS `polling_locations` (`localId` TEXT NOT NULL, `serverId` INTEGER NOT NULL, `name` TEXT NOT NULL, `wardName` TEXT NOT NULL, `wardId` INTEGER, `gpsCoordinates` TEXT NOT NULL, `scrutineerName` TEXT NOT NULL, `scrutineerCheckedIn` INTEGER NOT NULL, `securityRisk` TEXT NOT NULL, `expectedTurnout` INTEGER, `status` TEXT NOT NULL, `notes` TEXT NOT NULL, `ourTally` INTEGER, `updatedAt` TEXT NOT NULL, PRIMARY KEY(`localId`))");
        db.execSQL("CREATE INDEX IF NOT EXISTS `index_polling_locations_serverId` ON `polling_locations` (`serverId`)");
        db.execSQL("CREATE TABLE IF NOT EXISTS `sync_queue` (`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, `entityType` TEXT NOT NULL, `operation` TEXT NOT NULL, `serverId` INTEGER, `localId` TEXT NOT NULL, `payload` TEXT NOT NULL, `createdAt` INTEGER NOT NULL, `status` TEXT NOT NULL, `retryCount` INTEGER NOT NULL, `lastError` TEXT NOT NULL)");
        db.execSQL("CREATE INDEX IF NOT EXISTS `index_sync_queue_status` ON `sync_queue` (`status`)");
        db.execSQL("CREATE INDEX IF NOT EXISTS `index_sync_queue_entityType` ON `sync_queue` (`entityType`)");
        db.execSQL("CREATE TABLE IF NOT EXISTS room_master_table (id INTEGER PRIMARY KEY,identity_hash TEXT)");
        db.execSQL("INSERT OR REPLACE INTO room_master_table (id,identity_hash) VALUES(42, 'c1c6b31021bf0ecc7b0260254b953b0c')");
      }

      @Override
      public void dropAllTables(@NonNull final SupportSQLiteDatabase db) {
        db.execSQL("DROP TABLE IF EXISTS `supporters`");
        db.execSQL("DROP TABLE IF EXISTS `call_logs`");
        db.execSQL("DROP TABLE IF EXISTS `messages`");
        db.execSQL("DROP TABLE IF EXISTS `team_members`");
        db.execSQL("DROP TABLE IF EXISTS `influencers`");
        db.execSQL("DROP TABLE IF EXISTS `ward_profiles`");
        db.execSQL("DROP TABLE IF EXISTS `community_groups`");
        db.execSQL("DROP TABLE IF EXISTS `polling_locations`");
        db.execSQL("DROP TABLE IF EXISTS `sync_queue`");
        final List<? extends RoomDatabase.Callback> _callbacks = mCallbacks;
        if (_callbacks != null) {
          for (RoomDatabase.Callback _callback : _callbacks) {
            _callback.onDestructiveMigration(db);
          }
        }
      }

      @Override
      public void onCreate(@NonNull final SupportSQLiteDatabase db) {
        final List<? extends RoomDatabase.Callback> _callbacks = mCallbacks;
        if (_callbacks != null) {
          for (RoomDatabase.Callback _callback : _callbacks) {
            _callback.onCreate(db);
          }
        }
      }

      @Override
      public void onOpen(@NonNull final SupportSQLiteDatabase db) {
        mDatabase = db;
        internalInitInvalidationTracker(db);
        final List<? extends RoomDatabase.Callback> _callbacks = mCallbacks;
        if (_callbacks != null) {
          for (RoomDatabase.Callback _callback : _callbacks) {
            _callback.onOpen(db);
          }
        }
      }

      @Override
      public void onPreMigrate(@NonNull final SupportSQLiteDatabase db) {
        DBUtil.dropFtsSyncTriggers(db);
      }

      @Override
      public void onPostMigrate(@NonNull final SupportSQLiteDatabase db) {
      }

      @Override
      @NonNull
      public RoomOpenHelper.ValidationResult onValidateSchema(
          @NonNull final SupportSQLiteDatabase db) {
        final HashMap<String, TableInfo.Column> _columnsSupporters = new HashMap<String, TableInfo.Column>(20);
        _columnsSupporters.put("localId", new TableInfo.Column("localId", "TEXT", true, 1, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSupporters.put("serverId", new TableInfo.Column("serverId", "INTEGER", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSupporters.put("fullName", new TableInfo.Column("fullName", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSupporters.put("gender", new TableInfo.Column("gender", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSupporters.put("ageRange", new TableInfo.Column("ageRange", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSupporters.put("phone", new TableInfo.Column("phone", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSupporters.put("ward", new TableInfo.Column("ward", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSupporters.put("wardId", new TableInfo.Column("wardId", "INTEGER", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSupporters.put("village", new TableInfo.Column("village", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSupporters.put("villageId", new TableInfo.Column("villageId", "INTEGER", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSupporters.put("clan", new TableInfo.Column("clan", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSupporters.put("enrollmentStatus", new TableInfo.Column("enrollmentStatus", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSupporters.put("supportStatus", new TableInfo.Column("supportStatus", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSupporters.put("notes", new TableInfo.Column("notes", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSupporters.put("followUpRequired", new TableInfo.Column("followUpRequired", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSupporters.put("followUpDate", new TableInfo.Column("followUpDate", "TEXT", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSupporters.put("consentToMessages", new TableInfo.Column("consentToMessages", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSupporters.put("updatedAt", new TableInfo.Column("updatedAt", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSupporters.put("syncStatus", new TableInfo.Column("syncStatus", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSupporters.put("createdLocallyAt", new TableInfo.Column("createdLocallyAt", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        final HashSet<TableInfo.ForeignKey> _foreignKeysSupporters = new HashSet<TableInfo.ForeignKey>(0);
        final HashSet<TableInfo.Index> _indicesSupporters = new HashSet<TableInfo.Index>(2);
        _indicesSupporters.add(new TableInfo.Index("index_supporters_serverId", false, Arrays.asList("serverId"), Arrays.asList("ASC")));
        _indicesSupporters.add(new TableInfo.Index("index_supporters_syncStatus", false, Arrays.asList("syncStatus"), Arrays.asList("ASC")));
        final TableInfo _infoSupporters = new TableInfo("supporters", _columnsSupporters, _foreignKeysSupporters, _indicesSupporters);
        final TableInfo _existingSupporters = TableInfo.read(db, "supporters");
        if (!_infoSupporters.equals(_existingSupporters)) {
          return new RoomOpenHelper.ValidationResult(false, "supporters(com.campaignmasta.data.local.entity.SupporterEntity).\n"
                  + " Expected:\n" + _infoSupporters + "\n"
                  + " Found:\n" + _existingSupporters);
        }
        final HashMap<String, TableInfo.Column> _columnsCallLogs = new HashMap<String, TableInfo.Column>(18);
        _columnsCallLogs.put("localId", new TableInfo.Column("localId", "TEXT", true, 1, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCallLogs.put("serverId", new TableInfo.Column("serverId", "INTEGER", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCallLogs.put("personCalled", new TableInfo.Column("personCalled", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCallLogs.put("personType", new TableInfo.Column("personType", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCallLogs.put("phoneNumber", new TableInfo.Column("phoneNumber", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCallLogs.put("callDatetime", new TableInfo.Column("callDatetime", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCallLogs.put("callOutcome", new TableInfo.Column("callOutcome", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCallLogs.put("discussionSummary", new TableInfo.Column("discussionSummary", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCallLogs.put("issuesRaised", new TableInfo.Column("issuesRaised", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCallLogs.put("commitmentsMade", new TableInfo.Column("commitmentsMade", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCallLogs.put("followUpRequired", new TableInfo.Column("followUpRequired", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCallLogs.put("followUpDate", new TableInfo.Column("followUpDate", "TEXT", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCallLogs.put("influencerId", new TableInfo.Column("influencerId", "INTEGER", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCallLogs.put("supporterId", new TableInfo.Column("supporterId", "INTEGER", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCallLogs.put("callerId", new TableInfo.Column("callerId", "INTEGER", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCallLogs.put("updatedAt", new TableInfo.Column("updatedAt", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCallLogs.put("syncStatus", new TableInfo.Column("syncStatus", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCallLogs.put("createdLocallyAt", new TableInfo.Column("createdLocallyAt", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        final HashSet<TableInfo.ForeignKey> _foreignKeysCallLogs = new HashSet<TableInfo.ForeignKey>(0);
        final HashSet<TableInfo.Index> _indicesCallLogs = new HashSet<TableInfo.Index>(2);
        _indicesCallLogs.add(new TableInfo.Index("index_call_logs_serverId", false, Arrays.asList("serverId"), Arrays.asList("ASC")));
        _indicesCallLogs.add(new TableInfo.Index("index_call_logs_syncStatus", false, Arrays.asList("syncStatus"), Arrays.asList("ASC")));
        final TableInfo _infoCallLogs = new TableInfo("call_logs", _columnsCallLogs, _foreignKeysCallLogs, _indicesCallLogs);
        final TableInfo _existingCallLogs = TableInfo.read(db, "call_logs");
        if (!_infoCallLogs.equals(_existingCallLogs)) {
          return new RoomOpenHelper.ValidationResult(false, "call_logs(com.campaignmasta.data.local.entity.CallLogEntity).\n"
                  + " Expected:\n" + _infoCallLogs + "\n"
                  + " Found:\n" + _existingCallLogs);
        }
        final HashMap<String, TableInfo.Column> _columnsMessages = new HashMap<String, TableInfo.Column>(17);
        _columnsMessages.put("localId", new TableInfo.Column("localId", "TEXT", true, 1, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsMessages.put("serverId", new TableInfo.Column("serverId", "INTEGER", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsMessages.put("subject", new TableInfo.Column("subject", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsMessages.put("body", new TableInfo.Column("body", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsMessages.put("messageType", new TableInfo.Column("messageType", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsMessages.put("priority", new TableInfo.Column("priority", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsMessages.put("senderName", new TableInfo.Column("senderName", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsMessages.put("deliveryChannel", new TableInfo.Column("deliveryChannel", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsMessages.put("status", new TableInfo.Column("status", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsMessages.put("sentAt", new TableInfo.Column("sentAt", "TEXT", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsMessages.put("isRead", new TableInfo.Column("isRead", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsMessages.put("isAcknowledged", new TableInfo.Column("isAcknowledged", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsMessages.put("readReceiptRequired", new TableInfo.Column("readReceiptRequired", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsMessages.put("acknowledgementRequired", new TableInfo.Column("acknowledgementRequired", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsMessages.put("updatedAt", new TableInfo.Column("updatedAt", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsMessages.put("readSyncStatus", new TableInfo.Column("readSyncStatus", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsMessages.put("ackSyncStatus", new TableInfo.Column("ackSyncStatus", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        final HashSet<TableInfo.ForeignKey> _foreignKeysMessages = new HashSet<TableInfo.ForeignKey>(0);
        final HashSet<TableInfo.Index> _indicesMessages = new HashSet<TableInfo.Index>(1);
        _indicesMessages.add(new TableInfo.Index("index_messages_serverId", false, Arrays.asList("serverId"), Arrays.asList("ASC")));
        final TableInfo _infoMessages = new TableInfo("messages", _columnsMessages, _foreignKeysMessages, _indicesMessages);
        final TableInfo _existingMessages = TableInfo.read(db, "messages");
        if (!_infoMessages.equals(_existingMessages)) {
          return new RoomOpenHelper.ValidationResult(false, "messages(com.campaignmasta.data.local.entity.MessageEntity).\n"
                  + " Expected:\n" + _infoMessages + "\n"
                  + " Found:\n" + _existingMessages);
        }
        final HashMap<String, TableInfo.Column> _columnsTeamMembers = new HashMap<String, TableInfo.Column>(12);
        _columnsTeamMembers.put("localId", new TableInfo.Column("localId", "TEXT", true, 1, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsTeamMembers.put("serverId", new TableInfo.Column("serverId", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsTeamMembers.put("fullName", new TableInfo.Column("fullName", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsTeamMembers.put("gender", new TableInfo.Column("gender", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsTeamMembers.put("phone", new TableInfo.Column("phone", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsTeamMembers.put("email", new TableInfo.Column("email", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsTeamMembers.put("role", new TableInfo.Column("role", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsTeamMembers.put("wardName", new TableInfo.Column("wardName", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsTeamMembers.put("wardId", new TableInfo.Column("wardId", "INTEGER", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsTeamMembers.put("isActive", new TableInfo.Column("isActive", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsTeamMembers.put("notes", new TableInfo.Column("notes", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsTeamMembers.put("updatedAt", new TableInfo.Column("updatedAt", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        final HashSet<TableInfo.ForeignKey> _foreignKeysTeamMembers = new HashSet<TableInfo.ForeignKey>(0);
        final HashSet<TableInfo.Index> _indicesTeamMembers = new HashSet<TableInfo.Index>(1);
        _indicesTeamMembers.add(new TableInfo.Index("index_team_members_serverId", false, Arrays.asList("serverId"), Arrays.asList("ASC")));
        final TableInfo _infoTeamMembers = new TableInfo("team_members", _columnsTeamMembers, _foreignKeysTeamMembers, _indicesTeamMembers);
        final TableInfo _existingTeamMembers = TableInfo.read(db, "team_members");
        if (!_infoTeamMembers.equals(_existingTeamMembers)) {
          return new RoomOpenHelper.ValidationResult(false, "team_members(com.campaignmasta.data.local.entity.TeamMemberEntity).\n"
                  + " Expected:\n" + _infoTeamMembers + "\n"
                  + " Found:\n" + _existingTeamMembers);
        }
        final HashMap<String, TableInfo.Column> _columnsInfluencers = new HashMap<String, TableInfo.Column>(14);
        _columnsInfluencers.put("localId", new TableInfo.Column("localId", "TEXT", true, 1, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsInfluencers.put("serverId", new TableInfo.Column("serverId", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsInfluencers.put("fullName", new TableInfo.Column("fullName", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsInfluencers.put("phone", new TableInfo.Column("phone", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsInfluencers.put("communityRole", new TableInfo.Column("communityRole", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsInfluencers.put("influenceLevel", new TableInfo.Column("influenceLevel", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsInfluencers.put("relationshipStatus", new TableInfo.Column("relationshipStatus", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsInfluencers.put("contactFrequencyDays", new TableInfo.Column("contactFrequencyDays", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsInfluencers.put("lastCallDate", new TableInfo.Column("lastCallDate", "TEXT", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsInfluencers.put("nextContactDueDate", new TableInfo.Column("nextContactDueDate", "TEXT", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsInfluencers.put("wardName", new TableInfo.Column("wardName", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsInfluencers.put("wardId", new TableInfo.Column("wardId", "INTEGER", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsInfluencers.put("notes", new TableInfo.Column("notes", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsInfluencers.put("updatedAt", new TableInfo.Column("updatedAt", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        final HashSet<TableInfo.ForeignKey> _foreignKeysInfluencers = new HashSet<TableInfo.ForeignKey>(0);
        final HashSet<TableInfo.Index> _indicesInfluencers = new HashSet<TableInfo.Index>(1);
        _indicesInfluencers.add(new TableInfo.Index("index_influencers_serverId", false, Arrays.asList("serverId"), Arrays.asList("ASC")));
        final TableInfo _infoInfluencers = new TableInfo("influencers", _columnsInfluencers, _foreignKeysInfluencers, _indicesInfluencers);
        final TableInfo _existingInfluencers = TableInfo.read(db, "influencers");
        if (!_infoInfluencers.equals(_existingInfluencers)) {
          return new RoomOpenHelper.ValidationResult(false, "influencers(com.campaignmasta.data.local.entity.InfluencerEntity).\n"
                  + " Expected:\n" + _infoInfluencers + "\n"
                  + " Found:\n" + _existingInfluencers);
        }
        final HashMap<String, TableInfo.Column> _columnsWardProfiles = new HashMap<String, TableInfo.Column>(16);
        _columnsWardProfiles.put("localId", new TableInfo.Column("localId", "TEXT", true, 1, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsWardProfiles.put("serverId", new TableInfo.Column("serverId", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsWardProfiles.put("wardId", new TableInfo.Column("wardId", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsWardProfiles.put("wardName", new TableInfo.Column("wardName", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsWardProfiles.put("wardNumber", new TableInfo.Column("wardNumber", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsWardProfiles.put("llgName", new TableInfo.Column("llgName", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsWardProfiles.put("councillorName", new TableInfo.Column("councillorName", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsWardProfiles.put("supportStrength", new TableInfo.Column("supportStrength", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsWardProfiles.put("populationEstimate", new TableInfo.Column("populationEstimate", "INTEGER", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsWardProfiles.put("estimatedVotingPopulation", new TableInfo.Column("estimatedVotingPopulation", "INTEGER", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsWardProfiles.put("keyClans", new TableInfo.Column("keyClans", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsWardProfiles.put("keyChurches", new TableInfo.Column("keyChurches", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsWardProfiles.put("mainCommunityIssues", new TableInfo.Column("mainCommunityIssues", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsWardProfiles.put("notesForCandidate", new TableInfo.Column("notesForCandidate", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsWardProfiles.put("securityConcerns", new TableInfo.Column("securityConcerns", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsWardProfiles.put("updatedAt", new TableInfo.Column("updatedAt", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        final HashSet<TableInfo.ForeignKey> _foreignKeysWardProfiles = new HashSet<TableInfo.ForeignKey>(0);
        final HashSet<TableInfo.Index> _indicesWardProfiles = new HashSet<TableInfo.Index>(1);
        _indicesWardProfiles.add(new TableInfo.Index("index_ward_profiles_serverId", false, Arrays.asList("serverId"), Arrays.asList("ASC")));
        final TableInfo _infoWardProfiles = new TableInfo("ward_profiles", _columnsWardProfiles, _foreignKeysWardProfiles, _indicesWardProfiles);
        final TableInfo _existingWardProfiles = TableInfo.read(db, "ward_profiles");
        if (!_infoWardProfiles.equals(_existingWardProfiles)) {
          return new RoomOpenHelper.ValidationResult(false, "ward_profiles(com.campaignmasta.data.local.entity.WardProfileEntity).\n"
                  + " Expected:\n" + _infoWardProfiles + "\n"
                  + " Found:\n" + _existingWardProfiles);
        }
        final HashMap<String, TableInfo.Column> _columnsCommunityGroups = new HashMap<String, TableInfo.Column>(11);
        _columnsCommunityGroups.put("localId", new TableInfo.Column("localId", "TEXT", true, 1, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCommunityGroups.put("serverId", new TableInfo.Column("serverId", "INTEGER", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCommunityGroups.put("name", new TableInfo.Column("name", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCommunityGroups.put("groupType", new TableInfo.Column("groupType", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCommunityGroups.put("wardName", new TableInfo.Column("wardName", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCommunityGroups.put("wardId", new TableInfo.Column("wardId", "INTEGER", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCommunityGroups.put("estimatedVotingMembers", new TableInfo.Column("estimatedVotingMembers", "INTEGER", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCommunityGroups.put("alignment", new TableInfo.Column("alignment", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCommunityGroups.put("notes", new TableInfo.Column("notes", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCommunityGroups.put("updatedAt", new TableInfo.Column("updatedAt", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsCommunityGroups.put("syncStatus", new TableInfo.Column("syncStatus", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        final HashSet<TableInfo.ForeignKey> _foreignKeysCommunityGroups = new HashSet<TableInfo.ForeignKey>(0);
        final HashSet<TableInfo.Index> _indicesCommunityGroups = new HashSet<TableInfo.Index>(2);
        _indicesCommunityGroups.add(new TableInfo.Index("index_community_groups_serverId", false, Arrays.asList("serverId"), Arrays.asList("ASC")));
        _indicesCommunityGroups.add(new TableInfo.Index("index_community_groups_syncStatus", false, Arrays.asList("syncStatus"), Arrays.asList("ASC")));
        final TableInfo _infoCommunityGroups = new TableInfo("community_groups", _columnsCommunityGroups, _foreignKeysCommunityGroups, _indicesCommunityGroups);
        final TableInfo _existingCommunityGroups = TableInfo.read(db, "community_groups");
        if (!_infoCommunityGroups.equals(_existingCommunityGroups)) {
          return new RoomOpenHelper.ValidationResult(false, "community_groups(com.campaignmasta.data.local.entity.CommunityGroupEntity).\n"
                  + " Expected:\n" + _infoCommunityGroups + "\n"
                  + " Found:\n" + _existingCommunityGroups);
        }
        final HashMap<String, TableInfo.Column> _columnsPollingLocations = new HashMap<String, TableInfo.Column>(14);
        _columnsPollingLocations.put("localId", new TableInfo.Column("localId", "TEXT", true, 1, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsPollingLocations.put("serverId", new TableInfo.Column("serverId", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsPollingLocations.put("name", new TableInfo.Column("name", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsPollingLocations.put("wardName", new TableInfo.Column("wardName", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsPollingLocations.put("wardId", new TableInfo.Column("wardId", "INTEGER", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsPollingLocations.put("gpsCoordinates", new TableInfo.Column("gpsCoordinates", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsPollingLocations.put("scrutineerName", new TableInfo.Column("scrutineerName", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsPollingLocations.put("scrutineerCheckedIn", new TableInfo.Column("scrutineerCheckedIn", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsPollingLocations.put("securityRisk", new TableInfo.Column("securityRisk", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsPollingLocations.put("expectedTurnout", new TableInfo.Column("expectedTurnout", "INTEGER", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsPollingLocations.put("status", new TableInfo.Column("status", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsPollingLocations.put("notes", new TableInfo.Column("notes", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsPollingLocations.put("ourTally", new TableInfo.Column("ourTally", "INTEGER", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsPollingLocations.put("updatedAt", new TableInfo.Column("updatedAt", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        final HashSet<TableInfo.ForeignKey> _foreignKeysPollingLocations = new HashSet<TableInfo.ForeignKey>(0);
        final HashSet<TableInfo.Index> _indicesPollingLocations = new HashSet<TableInfo.Index>(1);
        _indicesPollingLocations.add(new TableInfo.Index("index_polling_locations_serverId", false, Arrays.asList("serverId"), Arrays.asList("ASC")));
        final TableInfo _infoPollingLocations = new TableInfo("polling_locations", _columnsPollingLocations, _foreignKeysPollingLocations, _indicesPollingLocations);
        final TableInfo _existingPollingLocations = TableInfo.read(db, "polling_locations");
        if (!_infoPollingLocations.equals(_existingPollingLocations)) {
          return new RoomOpenHelper.ValidationResult(false, "polling_locations(com.campaignmasta.data.local.entity.PollingLocationEntity).\n"
                  + " Expected:\n" + _infoPollingLocations + "\n"
                  + " Found:\n" + _existingPollingLocations);
        }
        final HashMap<String, TableInfo.Column> _columnsSyncQueue = new HashMap<String, TableInfo.Column>(10);
        _columnsSyncQueue.put("id", new TableInfo.Column("id", "INTEGER", true, 1, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSyncQueue.put("entityType", new TableInfo.Column("entityType", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSyncQueue.put("operation", new TableInfo.Column("operation", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSyncQueue.put("serverId", new TableInfo.Column("serverId", "INTEGER", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSyncQueue.put("localId", new TableInfo.Column("localId", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSyncQueue.put("payload", new TableInfo.Column("payload", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSyncQueue.put("createdAt", new TableInfo.Column("createdAt", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSyncQueue.put("status", new TableInfo.Column("status", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSyncQueue.put("retryCount", new TableInfo.Column("retryCount", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSyncQueue.put("lastError", new TableInfo.Column("lastError", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        final HashSet<TableInfo.ForeignKey> _foreignKeysSyncQueue = new HashSet<TableInfo.ForeignKey>(0);
        final HashSet<TableInfo.Index> _indicesSyncQueue = new HashSet<TableInfo.Index>(2);
        _indicesSyncQueue.add(new TableInfo.Index("index_sync_queue_status", false, Arrays.asList("status"), Arrays.asList("ASC")));
        _indicesSyncQueue.add(new TableInfo.Index("index_sync_queue_entityType", false, Arrays.asList("entityType"), Arrays.asList("ASC")));
        final TableInfo _infoSyncQueue = new TableInfo("sync_queue", _columnsSyncQueue, _foreignKeysSyncQueue, _indicesSyncQueue);
        final TableInfo _existingSyncQueue = TableInfo.read(db, "sync_queue");
        if (!_infoSyncQueue.equals(_existingSyncQueue)) {
          return new RoomOpenHelper.ValidationResult(false, "sync_queue(com.campaignmasta.data.local.entity.SyncQueueEntity).\n"
                  + " Expected:\n" + _infoSyncQueue + "\n"
                  + " Found:\n" + _existingSyncQueue);
        }
        return new RoomOpenHelper.ValidationResult(true, null);
      }
    }, "c1c6b31021bf0ecc7b0260254b953b0c", "946a8337bac5dea6ccf5923374f57c57");
    final SupportSQLiteOpenHelper.Configuration _sqliteConfig = SupportSQLiteOpenHelper.Configuration.builder(config.context).name(config.name).callback(_openCallback).build();
    final SupportSQLiteOpenHelper _helper = config.sqliteOpenHelperFactory.create(_sqliteConfig);
    return _helper;
  }

  @Override
  @NonNull
  protected InvalidationTracker createInvalidationTracker() {
    final HashMap<String, String> _shadowTablesMap = new HashMap<String, String>(0);
    final HashMap<String, Set<String>> _viewTables = new HashMap<String, Set<String>>(0);
    return new InvalidationTracker(this, _shadowTablesMap, _viewTables, "supporters","call_logs","messages","team_members","influencers","ward_profiles","community_groups","polling_locations","sync_queue");
  }

  @Override
  public void clearAllTables() {
    super.assertNotMainThread();
    final SupportSQLiteDatabase _db = super.getOpenHelper().getWritableDatabase();
    try {
      super.beginTransaction();
      _db.execSQL("DELETE FROM `supporters`");
      _db.execSQL("DELETE FROM `call_logs`");
      _db.execSQL("DELETE FROM `messages`");
      _db.execSQL("DELETE FROM `team_members`");
      _db.execSQL("DELETE FROM `influencers`");
      _db.execSQL("DELETE FROM `ward_profiles`");
      _db.execSQL("DELETE FROM `community_groups`");
      _db.execSQL("DELETE FROM `polling_locations`");
      _db.execSQL("DELETE FROM `sync_queue`");
      super.setTransactionSuccessful();
    } finally {
      super.endTransaction();
      _db.query("PRAGMA wal_checkpoint(FULL)").close();
      if (!_db.inTransaction()) {
        _db.execSQL("VACUUM");
      }
    }
  }

  @Override
  @NonNull
  protected Map<Class<?>, List<Class<?>>> getRequiredTypeConverters() {
    final HashMap<Class<?>, List<Class<?>>> _typeConvertersMap = new HashMap<Class<?>, List<Class<?>>>();
    _typeConvertersMap.put(SupporterDao.class, SupporterDao_Impl.getRequiredConverters());
    _typeConvertersMap.put(CallLogDao.class, CallLogDao_Impl.getRequiredConverters());
    _typeConvertersMap.put(MessageDao.class, MessageDao_Impl.getRequiredConverters());
    _typeConvertersMap.put(TeamMemberDao.class, TeamMemberDao_Impl.getRequiredConverters());
    _typeConvertersMap.put(InfluencerDao.class, InfluencerDao_Impl.getRequiredConverters());
    _typeConvertersMap.put(WardProfileDao.class, WardProfileDao_Impl.getRequiredConverters());
    _typeConvertersMap.put(CommunityGroupDao.class, CommunityGroupDao_Impl.getRequiredConverters());
    _typeConvertersMap.put(PollingLocationDao.class, PollingLocationDao_Impl.getRequiredConverters());
    _typeConvertersMap.put(SyncQueueDao.class, SyncQueueDao_Impl.getRequiredConverters());
    return _typeConvertersMap;
  }

  @Override
  @NonNull
  public Set<Class<? extends AutoMigrationSpec>> getRequiredAutoMigrationSpecs() {
    final HashSet<Class<? extends AutoMigrationSpec>> _autoMigrationSpecsSet = new HashSet<Class<? extends AutoMigrationSpec>>();
    return _autoMigrationSpecsSet;
  }

  @Override
  @NonNull
  public List<Migration> getAutoMigrations(
      @NonNull final Map<Class<? extends AutoMigrationSpec>, AutoMigrationSpec> autoMigrationSpecs) {
    final List<Migration> _autoMigrations = new ArrayList<Migration>();
    return _autoMigrations;
  }

  @Override
  public SupporterDao supporterDao() {
    if (_supporterDao != null) {
      return _supporterDao;
    } else {
      synchronized(this) {
        if(_supporterDao == null) {
          _supporterDao = new SupporterDao_Impl(this);
        }
        return _supporterDao;
      }
    }
  }

  @Override
  public CallLogDao callLogDao() {
    if (_callLogDao != null) {
      return _callLogDao;
    } else {
      synchronized(this) {
        if(_callLogDao == null) {
          _callLogDao = new CallLogDao_Impl(this);
        }
        return _callLogDao;
      }
    }
  }

  @Override
  public MessageDao messageDao() {
    if (_messageDao != null) {
      return _messageDao;
    } else {
      synchronized(this) {
        if(_messageDao == null) {
          _messageDao = new MessageDao_Impl(this);
        }
        return _messageDao;
      }
    }
  }

  @Override
  public TeamMemberDao teamMemberDao() {
    if (_teamMemberDao != null) {
      return _teamMemberDao;
    } else {
      synchronized(this) {
        if(_teamMemberDao == null) {
          _teamMemberDao = new TeamMemberDao_Impl(this);
        }
        return _teamMemberDao;
      }
    }
  }

  @Override
  public InfluencerDao influencerDao() {
    if (_influencerDao != null) {
      return _influencerDao;
    } else {
      synchronized(this) {
        if(_influencerDao == null) {
          _influencerDao = new InfluencerDao_Impl(this);
        }
        return _influencerDao;
      }
    }
  }

  @Override
  public WardProfileDao wardProfileDao() {
    if (_wardProfileDao != null) {
      return _wardProfileDao;
    } else {
      synchronized(this) {
        if(_wardProfileDao == null) {
          _wardProfileDao = new WardProfileDao_Impl(this);
        }
        return _wardProfileDao;
      }
    }
  }

  @Override
  public CommunityGroupDao communityGroupDao() {
    if (_communityGroupDao != null) {
      return _communityGroupDao;
    } else {
      synchronized(this) {
        if(_communityGroupDao == null) {
          _communityGroupDao = new CommunityGroupDao_Impl(this);
        }
        return _communityGroupDao;
      }
    }
  }

  @Override
  public PollingLocationDao pollingLocationDao() {
    if (_pollingLocationDao != null) {
      return _pollingLocationDao;
    } else {
      synchronized(this) {
        if(_pollingLocationDao == null) {
          _pollingLocationDao = new PollingLocationDao_Impl(this);
        }
        return _pollingLocationDao;
      }
    }
  }

  @Override
  public SyncQueueDao syncQueueDao() {
    if (_syncQueueDao != null) {
      return _syncQueueDao;
    } else {
      synchronized(this) {
        if(_syncQueueDao == null) {
          _syncQueueDao = new SyncQueueDao_Impl(this);
        }
        return _syncQueueDao;
      }
    }
  }
}
